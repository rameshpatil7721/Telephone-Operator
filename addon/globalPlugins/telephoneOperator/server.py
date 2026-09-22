from flask import Flask, request, jsonify
from werkzeug.serving import make_server, WSGIRequestHandler
import socket
import qrcode
import webbrowser
import base64
import io
import threading
import secrets

app = Flask(__name__)

SECRET_KEY = None
latest_number = None
history = []

server_instance = None
server_thread = None


class SilentRequestHandler(WSGIRequestHandler):
    """Suppress routine HTTP access logging."""

    def log_request(self, code="-", size="-"):
        pass

# =========================
# Auto detect local IP
# =========================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# =========================
# Receive number from NVDA
# =========================
@app.route("/call")
def call():
    global latest_number, history

    key = request.args.get("key")
    number = request.args.get("number")

    if not SECRET_KEY or key != SECRET_KEY:
        return "Unauthorized", 403

    if not number:
        return "No number provided", 400

    number = number.strip().replace(" ", "").replace("-", "")

    latest_number = number

    if number in history:
        history.remove(number)
    history.insert(0, number)
    history = history[:5]

    return "OK"


# =========================
# APIs
# =========================
@app.route("/get_number")
def get_number():
    return jsonify({"number": latest_number})


@app.route("/get_history")
def get_history():
    return jsonify({"history": history})


# =========================
# MAIN UI (unchanged)
# =========================
@app.route("/")
def home():
    return """<!DOCTYPE html>
<html>
<head>
<title>Dialer</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {font-family: Arial;text-align: center;padding: 20px;background: #f2f2f2;}
.dark {background: #121212;color: #fff;}
#number {font-size: 34px;margin: 25px 0;font-weight: bold;}
button {font-size: 26px;padding: 18px 35px;border-radius: 10px;border: none;background: #28a745;color: white;margin: 10px;}
button:focus {outline: 3px solid #ff9800;}
.toggle {background: #007AFF;}
.history {margin-top: 20px;text-align: left;}
.history-item {padding: 10px;border-bottom: 1px solid #ccc;}
a {text-decoration: none;font-size: 20px;}
</style>
</head>
<body>

<h2>📞 Ready to Call</h2>

<div id="number">Waiting for number...</div>

<button id="callBtn" onclick="makeCall()">CALL</button><br>
<button class="toggle" onclick="toggleDark()">Toggle Dark Mode</button>
<button class="toggle" onclick="toggleHistory()">History</button>

<div id="historyBox" class="history" style="display:none;"></div>

<div aria-live="assertive" id="live" style="position:absolute; left:-9999px;"></div>

<script>
let currentNumber = "";

window.onload = () => {
    document.getElementById("callBtn").focus();
    if(localStorage.getItem("dark") === "true"){
        document.body.classList.add("dark");
    }
};

setInterval(async () => {
    try {
        let res = await fetch('/get_number');
        let data = await res.json();

        if (data.number && data.number !== currentNumber) {
            currentNumber = data.number;
            document.getElementById("number").innerText = currentNumber;
            document.getElementById("live").innerText = "New number " + currentNumber;
            document.getElementById("callBtn").focus();
        }
    } catch(e){}
}, 1000);

function makeCall() {
    if (currentNumber) {
        window.location.href = "tel:" + currentNumber;
    }
}

function toggleDark(){
    document.body.classList.toggle("dark");
    localStorage.setItem("dark", document.body.classList.contains("dark"));
}

async function toggleHistory(){
    let box = document.getElementById("historyBox");

    if(box.style.display === "none"){
        let res = await fetch('/get_history');
        let data = await res.json();

        let html = "<h3>Last 5 Numbers</h3>";
        data.history.forEach(num => {
            html += `<div class="history-item"><a href="tel:${num}">${num}</a></div>`;
        });

        box.innerHTML = html;
        box.style.display = "block";
    } else {
        box.style.display = "none";
    }
}
</script>

</body>
</html>
"""


# =========================
# QR SETUP PAGE (NEW)
# =========================
@app.route("/qr")
def qr_page():
    ip = get_local_ip()
    url = f"http://{ip}:5000"

    img = qrcode.make(url)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return f"""
    <html>
    <head>
        <title>Dialer Setup</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: Arial;
                text-align: center;
                padding: 30px;
            }}
            img {{
                width: 250px;
                height: 250px;
            }}
            .url {{
                font-size: 20px;
                margin-top: 20px;
                word-break: break-all;
            }}
            button {{
                font-size: 18px;
                padding: 10px 20px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>

    <h2>📞 Dialer Setup</h2>

    <p>Scan this QR code with your phone:</p>

    <img src="data:image/png;base64,{img_str}" />

    <div class="url">
        Or open this link:<br>
        <a id="link" href="{url}">{url}</a>
    </div>

    <button onclick="copyLink()">Copy Link</button>

    <p style="margin-top:20px;">
        Keep this page open on your phone for calling.
    </p>

    <script>
    function copyLink() {{
        const url = document.getElementById("link").innerText;
        navigator.clipboard.writeText(url);
        alert("Link copied to clipboard");
    }}
    </script>

    </body>
    </html>
    """

# =========================
# SERVER CONTROL
# =========================

def start_server():
    global server_instance
    global server_thread
    global SECRET_KEY

    if server_instance is not None:
        return False

    # Generate a new temporary authentication key
    # every time Telephone Operator is started.
    SECRET_KEY = secrets.token_urlsafe(32)

    server_instance = make_server(
        "0.0.0.0",
        5000,
        app,
        threaded=True,
        request_handler=SilentRequestHandler
    )

    server_thread = threading.Thread(
        target=server_instance.serve_forever,
        daemon=True
    )

    server_thread.start()

    return True

def stop_server():
    global server_instance
    global server_thread
    global SECRET_KEY

    if server_instance is None:
        return False

    server_instance.shutdown()

    if server_thread is not None:
        server_thread.join(timeout=3)

    server_instance = None
    server_thread = None
    SECRET_KEY = None

    return True

# =========================
# RUN SERVER
# =========================
if __name__ == "__main__":
    ip = get_local_ip()
    url = f"http://{ip}:5000"
    qr_url = f"http://{ip}:5000/qr"

    print("\n==============================")
    print("📞 Dialer Server Started")
    print(f"👉 Open on phone: {url}")
    print(f"👉 Setup page: {qr_url}")
    print("==============================\n")

    # Open browser automatically
    webbrowser.open(qr_url)

    app.run(host="0.0.0.0", port=5000)