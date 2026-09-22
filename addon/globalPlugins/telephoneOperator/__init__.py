import os
import sys
import ui
import logHandler

PLUGIN_PATH = os.path.dirname(__file__)

LIB_PATH = os.path.join(
    PLUGIN_PATH,
    "lib"
)

if PLUGIN_PATH not in sys.path:
    sys.path.insert(0, PLUGIN_PATH)

if LIB_PATH not in sys.path:
    sys.path.insert(0, LIB_PATH)

log = logHandler.log


import globalPluginHandler
import api
import ui
import logHandler
import urllib.request
import urllib.error
import urllib.parse
import re
import wx
import time
import scriptHandler
import keyboardHandler
import controlTypes
import gui


SERVER_IP = "127.0.0.1"
PORT = 5000

# Short timeout for checking whether Flask is running.
SERVER_CHECK_TIMEOUT = 1

# Timeout for the actual call request.
CALL_TIMEOUT = 2

log = logHandler.log

from dialerUI import PhoneDialerDialog, InstructionsDialog


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

    scriptCategory = "Telephone Operator"

    def __init__(self):

        super().__init__()

        self.phoneDialerDialog = None

        self.telephoneOperatorMenu = wx.Menu()

        self.startMenuItem = self.telephoneOperatorMenu.Append(
            wx.ID_ANY,
            "Start Telephone Operator"
        )

        self.stopMenuItem = self.telephoneOperatorMenu.Append(
            wx.ID_ANY,
            "Stop Telephone Operator"
        )

        self.telephoneOperatorMenu.AppendSeparator()

        self.instructionsMenuItem = self.telephoneOperatorMenu.Append(
            wx.ID_ANY,
            "Instructions"
        )

        # ---------------------------------------------------------
        # Add Telephone Operator under NVDA -> Tools.
        #
        # NVDA does not expose a "toolsMenu" attribute on the main
        # menu, so find the existing Tools submenu directly.
        # ---------------------------------------------------------

        mainMenu = gui.mainFrame.sysTrayIcon.menu
        toolsMenu = None

        for menuItem in mainMenu.GetMenuItems():

            if menuItem.GetItemLabelText() == "Tools":

                toolsMenu = menuItem.GetSubMenu()
                break

        if toolsMenu is None:

            log.error(
                "Telephone Operator: Unable to find NVDA Tools menu"
            )

            raise RuntimeError(
                "Unable to find NVDA Tools menu"
            )

        self.telephoneOperatorMenuRoot = (
            toolsMenu.AppendSubMenu(
                self.telephoneOperatorMenu,
                "Telephone Operator"
            )
        )

        self.telephoneOperatorMenu.Bind(
            wx.EVT_MENU,
            self.onStartMenu,
            self.startMenuItem
        )

        self.telephoneOperatorMenu.Bind(
            wx.EVT_MENU,
            self.onStopMenu,
            self.stopMenuItem
        )

        self.telephoneOperatorMenu.Bind(
            wx.EVT_MENU,
            self.onInstructionsMenu,
            self.instructionsMenuItem
        )

        # Set the initial menu state.
        self._updateMenuState()


    def _updateMenuState(self):

        import server

        try:

            if server.server_instance is None:

                # Server is stopped.
                self.startMenuItem.Enable(True)
                self.stopMenuItem.Enable(False)

                log.debug(
                    "Telephone Operator: Menu state updated - server stopped"
                )

            else:

                # Server is running.
                self.startMenuItem.Enable(False)
                self.stopMenuItem.Enable(True)

                log.debug(
                    "Telephone Operator: Menu state updated - server running"
                )

        except Exception:

            log.exception(
                "Telephone Operator: Failed to update menu state"
            )


    def _stopServer(self, menu=False):

        import server

        try:

            if server.server_instance is None:

                log.info(
                    "Telephone Operator: Server is not running"
                )

                # Keep menu state correct.
                self._updateMenuState()

                if menu:
                    wx.CallLater(
                        50,
                        ui.message,
                        "Telephone Operator is not running",
                        speechPriority=1
                    )
                else:
                    ui.message(
                        "Telephone Operator is not running"
                    )

                return

            stopped = server.stop_server()

            # Close the Telephone Operator dialog if it is open
            if self.phoneDialerDialog is not None:
                try:
                    if self.phoneDialerDialog.IsShown():
                        self.phoneDialerDialog.EndModal(wx.ID_CANCEL)
                except Exception:
                    log.exception(
                        "Telephone Operator: Error closing start dialog"
                    )

            if stopped:

                log.info(
                    "Telephone Operator: Flask server stopped"
                )

                # Server is now stopped.
                self._updateMenuState()

                if menu:
                    wx.CallLater(
                        100,
                        ui.message,
                        "Telephone Operator stopped",
                        speechPriority=1
                    )
                else:
                    wx.CallLater(
                        100,
                        ui.message,
                        "Telephone Operator stopped"
                    )

            else:

                # Make sure menu state reflects actual server state.
                self._updateMenuState()

                if menu:
                    ui.delayedMessage(
                        "Telephone Operator is not running"
                    )
                else:
                    ui.message(
                        "Telephone Operator is not running"
                    )

        except Exception:

            log.exception(
                "Telephone Operator: Failed to stop Flask server"
            )

            self._updateMenuState()

            if menu:
                ui.delayedMessage(
                    "Unable to stop Telephone Operator"
                )
            else:
                ui.message(
                    "Unable to stop Telephone Operator"
                )


    def onStartMenu(self, event):

        self._startServer(menu=True)


    def onStopMenu(self, event):

        self._stopServer(menu=True)


    def onInstructionsMenu(self, event):

        try:

            dialog = InstructionsDialog(
                gui.mainFrame
            )

            dialog.ShowModal()
            dialog.Destroy()

        except Exception:

            log.exception(
                "Telephone Operator: Failed to show instructions"
            )

            ui.message("Unable to open instructions")


    def _is_server_available(self):
        """
        Check whether the local Flask call server is running.
        """

        url = f"http://{SERVER_IP}:{PORT}/get_number"

        try:
            response = urllib.request.urlopen(
                url,
                timeout=SERVER_CHECK_TIMEOUT
            )

            try:
                if response.status == 200:
                    log.debug(
                        "Call server availability check successful"
                    )
                    return True

                log.warning(
                    "Call server availability check returned HTTP %s",
                    response.status
                )
                return False

            finally:
                response.close()

        except urllib.error.URLError as e:
            log.debug(
                "Call server is not reachable: %s",
                e
            )
            return False

        except Exception:
            log.exception(
                "Unexpected error while checking call server"
            )
            return False


    def _get_selected_text(self, obj):
        """
        Try to obtain real selected text.

        Order:
        1. Focused object selection
        2. Document tree interceptor selection
        """

        # 1. Normal application selection
        try:
            info = obj.makeTextInfo("selection")
            text = info.text

            if text and text.strip():
                log.debug(
                    "Text obtained from focused-object selection"
                )
                return text

        except Exception:
            log.debug(
                "Focused-object selection unavailable",
                exc_info=True
            )

        # 2. Browser / document selection
        try:
            tree = getattr(obj, "treeInterceptor", None)

            if tree:
                info = tree.makeTextInfo("selection")
                text = info.text

                if text and text.strip():
                    log.debug(
                        "Text obtained from document tree selection"
                    )
                    return text

        except Exception:
            log.debug(
                "Document tree selection unavailable",
                exc_info=True
            )

        return ""


    def _get_focused_text(self, obj):
        """
        Get text associated with the currently focused object.

        Important for Excel cells and normal controls.
        """

        try:
            value = getattr(obj, "value", None)

            if value and str(value).strip():
                log.debug(
                    "Text obtained from focused object value"
                )
                return str(value)

        except Exception:
            log.debug(
                "Unable to read focused object value",
                exc_info=True
            )

        try:
            name = getattr(obj, "name", None)

            if name and str(name).strip():
                log.debug(
                    "Text obtained from focused object name"
                )
                return str(name)

        except Exception:
            log.debug(
                "Unable to read focused object name",
                exc_info=True
            )

        return ""


    def _get_review_line(self):
        """
        Get only the current review line.

        We intentionally do NOT use review.text directly because
        in browser document review it can represent a large portion
        of the webpage and may contain many unrelated numbers.
        """

        try:
            review = api.getReviewPosition()

            line = review.copy()
            line.expand("line")

            text = line.text

            if text and text.strip():
                log.debug(
                    "Text obtained from review cursor line"
                )
                return text

        except Exception:
            log.debug(
                "Unable to obtain review cursor line",
                exc_info=True
            )

        return ""


    def _get_clipboard_text(self):
        """
        Use Ctrl+C as a fallback.

        This follows the approach used by the Sarvam plugin.
        """

        try:
            keyboardHandler.KeyboardInputGesture.fromName(
                "control+c"
            ).send()

            time.sleep(0.1)

            if wx.TheClipboard.Open():
                try:
                    data = wx.TextDataObject()

                    if wx.TheClipboard.GetData(data):
                        text = data.GetText()

                        if text and text.strip():
                            log.debug(
                                "Text obtained from clipboard fallback"
                            )
                            return text

                finally:
                    wx.TheClipboard.Close()

        except Exception:
            log.debug(
                "Clipboard fallback failed",
                exc_info=True
            )

        return ""


    def _find_phone_numbers(self, text):
        """
        Find number candidates containing 2 to 15 digits.

        Spaces and hyphens between digits are allowed.

        Examples:
            9876543210
            98765 43210
            98765-43210
            +91 98765 43210
            +91-98765-43210
            112
            100
        """

        if not text:
            return []

        text = str(text)

        # Do not allow newline characters inside a phone-number
        # candidate.
        pattern = r"(?<!\d)\+?\d(?:[ \t-]*\d){1,14}(?!\d)"

        matches = re.findall(pattern, text)

        numbers = []

        for match in matches:

            # Remove spaces and hyphens.
            number = re.sub(r"[ \t-]", "", match)

            # Keep + only at the beginning.
            if number.startswith("+"):
                digits = number[1:]
            else:
                digits = number

            # Allow 2 to 15 digits.
            if 2 <= len(digits) <= 15:

                if number not in numbers:
                    numbers.append(number)

        log.debug(
            "Phone-number extraction found %d candidate(s)",
            len(numbers)
        )

        return numbers


    def _send_number(self, number):
        """
        Send the cleaned number to the local Flask server.
        """

        import server

        if not server.SECRET_KEY:
            log.warning(
                "Telephone Operator: Authentication key is not available"
            )

            ui.message(
                "Telephone Operator is not reachable"
            )

            return False

        params = urllib.parse.urlencode({
            "number": number,
            "key": server.SECRET_KEY
        })

        url = f"http://{SERVER_IP}:{PORT}/call?{params}"

        try:
            response = urllib.request.urlopen(
                url,
                timeout=CALL_TIMEOUT
            )

            try:
                if response.status == 200:

                    # Do not log the actual phone number.
                    log.debug(
                        "Phone number successfully sent to Telephone Operator"
                    )

                    ui.message(
                        f"Sending number {number} to phone"
                    )

                    return True

                log.warning(
                    "Call request returned HTTP %s",
                    response.status
                )

                ui.message(
                    "Telephone Operator is not reachable"
                )
                return False

            finally:
                response.close()

        except urllib.error.URLError as e:

            log.warning(
                "Call request failed because server is unreachable: %s",
                e
            )

            ui.message(
                "Telephone Operator is not reachable"
            )
            return False

        except Exception:

            log.exception(
                "Unexpected error while sending call request"
            )

            ui.message(
                "Telephone Operator is not reachable"
            )
            return False


    def _process_text(self, text):
        """
        Process text and determine whether it contains:

        0 numbers  -> Phone number not found
        1 number   -> send it
        2+ numbers -> ask user to select one
        """

        if not text or not str(text).strip():
            return False

        numbers = self._find_phone_numbers(text)

        if not numbers:
            ui.message("Phone number not found")
            return True

        if len(numbers) > 1:

            log.info(
                "Multiple phone-number candidates detected: %d",
                len(numbers)
            )

            ui.message(
                "Multiple phone numbers found. "
                "Please select one."
            )

            return True

        self._send_number(numbers[0])
        return True


    def script_callNumber(self, gesture):
        """
        Send the selected or focused phone number to the connected phone.
        """
        log.debug(
            "Call shortcut triggered"
        )

        try:

            # ---------------------------------------------------------
            # STEP 0
            # Check the call server FIRST.
            # ---------------------------------------------------------

            if not self._is_server_available():

                ui.message(
                    "Telephone Operator is not reachable"
                )

                log.debug(
                    "Call operation stopped because server is unavailable"
                )

                return


            obj = api.getFocusObject()

            log.debug(
                "Focused object obtained: %s",
                type(obj).__name__
            )

            # ---------------------------------------------------------
            # EXCEL BLANK CELL CHECK
            #
            # If the focused Excel cell is blank, stop here.
            # This prevents review/clipboard fallback from picking up
            # unrelated numbers from elsewhere.
            # ---------------------------------------------------------

            try:
                focused_role = obj.role

                if focused_role == controlTypes.Role.TABLECELL:
                    focused_value = getattr(obj, "value", None)
                    focused_name = getattr(obj, "name", None)

                    if not focused_value and not focused_name:
                        log.debug(
                            "Blank Excel cell detected"
                        )
                        ui.message("No Data")
                        return

            except Exception:
                log.debug(
                    "Excel blank-cell check unavailable",
                    exc_info=True
                )


            # ---------------------------------------------------------
            # STEP 1
            # Actual selection.
            #
            # This always has highest priority.
            # ---------------------------------------------------------

            selected_text = self._get_selected_text(obj)

            if selected_text:

                log.debug(
                    "Processing selected text"
                )

                self._process_text(selected_text)
                return


            # ---------------------------------------------------------
            # STEP 2
            # No selection.
            #
            # First examine the focused object.
            # Important for Excel.
            #
            # IMPORTANT CHANGE:
            # If the focused object has useful text, it is treated
            # as the current source. We do NOT fall through to the
            # clipboard if this text contains no phone number.
            # ---------------------------------------------------------

            focused_text = self._get_focused_text(obj)

            if focused_text:

                log.debug(
                    "Processing focused object text"
                )

                numbers = self._find_phone_numbers(
                    focused_text
                )

                if numbers:

                    if len(numbers) > 1:

                        log.debug(
                            "Multiple phone-number candidates "
                            "found in focused object: %d",
                            len(numbers)
                        )

                        ui.message(
                            "Multiple phone numbers found. "
                            "Please select one."
                        )

                        return

                    self._send_number(numbers[0])
                    return

                # IMPORTANT:
                # The current object contains text, but no phone
                # number. Do not use old clipboard contents.
                log.debug(
                    "Focused object contains text but no phone number"
                )

                ui.message("Phone number not found")
                return


            # ---------------------------------------------------------
            # STEP 3
            # Review cursor current line.
            # ---------------------------------------------------------

            review_text = self._get_review_line()

            if review_text:

                log.debug(
                    "Processing review cursor line"
                )

                numbers = self._find_phone_numbers(
                    review_text
                )

                if numbers:

                    if len(numbers) > 1:

                        log.info(
                            "Multiple phone-number candidates "
                            "found in review line: %d",
                            len(numbers)
                        )

                        ui.message(
                            "Multiple phone numbers found. "
                            "Please select one."
                        )

                        return

                    self._send_number(numbers[0])
                    return


            # ---------------------------------------------------------
            # STEP 4
            # Clipboard fallback.
            #
            # Clipboard is reached only when there is no useful
            # focused-object text.
            #
            # This preserves webpage/other-application fallback
            # behavior while preventing stale clipboard data from
            # overriding a text-only Excel cell.
            # ---------------------------------------------------------

            clipboard_text = self._get_clipboard_text()

            if clipboard_text:

                log.debug(
                    "Processing clipboard text"
                )

                numbers = self._find_phone_numbers(
                    clipboard_text
                )

                if numbers:

                    if len(numbers) > 1:

                        log.info(
                            "Multiple phone-number candidates "
                            "found in clipboard: %d",
                            len(numbers)
                        )

                        ui.message(
                            "Multiple phone numbers found. "
                            "Please select one."
                        )

                        return

                    self._send_number(numbers[0])
                    return


            # ---------------------------------------------------------
            # STEP 5
            # Nothing useful found.
            # ---------------------------------------------------------

            log.debug(
                "No phone number found"
            )

            ui.message("Phone number not found")


        except Exception:

            log.exception(
                "Unexpected error while processing call shortcut"
            )

            ui.message("Error processing phone number")


    def _showPhoneDialerDialog(self, phone_url, qr_url):
        try:
            self.phoneDialerDialog = PhoneDialerDialog(
                gui.mainFrame,
                phone_url,
                qr_url
            )

            self.phoneDialerDialog.ShowModal()

            if self.phoneDialerDialog is not None:
                self.phoneDialerDialog.Destroy()
                self.phoneDialerDialog = None

        except Exception:
            log.exception("Telephone Operator: Error showing start dialog")
            ui.message("Telephone Operator started")

    def _startServer(self, menu=False):

        import server

        log.info(
            "Telephone Operator: Starting server"
        )

        # ---------------------------------------------------------
        # Check whether server is already running.
        # ---------------------------------------------------------

        if self._is_server_available():

            log.info(
                "Telephone Operator: Flask server is already running"
            )

            # Keep menu state correct.
            self._updateMenuState()

            if menu:
                ui.delayedMessage(
                    "Telephone Operator is already running"
                )
            else:
                ui.message(
                    "Telephone Operator is already running"
                )

            return

        # ---------------------------------------------------------
        # Start Flask server.
        # ---------------------------------------------------------

        try:

            started = server.start_server()

            if not started:

                log.info(
                    "Telephone Operator: Flask server was already running"
                )

                self._updateMenuState()

                if menu:
                    ui.delayedMessage(
                        "Telephone Operator is already running"
                    )
                else:
                    ui.message(
                        "Telephone Operator is already running"
                    )

                return

        except Exception:

            log.exception(
                "Telephone Operator: Failed to start Flask server"
            )

            self._updateMenuState()

            if menu:
                ui.delayedMessage(
                    "Unable to start Telephone Operator"
                )
            else:
                ui.message(
                    "Unable to start Telephone Operator"
                )

            return

        # ---------------------------------------------------------
        # Wait for Flask to become available.
        # ---------------------------------------------------------

        for attempt in range(10):

            time.sleep(0.5)

            if self._is_server_available():

                log.info(
                    "Telephone Operator: Flask server is ready"
                )

                try:

                    phone_ip = server.get_local_ip()

                    phone_url = (
                        "http://"
                        + phone_ip
                        + ":5000"
                    )

                    qr_url = phone_url + "/qr"

                    log.info(
                        "Telephone Operator: Telephone Operator address prepared"
                    )

                    # Server is now running, so update menu.
                    self._updateMenuState()

                    wx.CallAfter(
                        self._showPhoneDialerDialog,
                        phone_url,
                        qr_url
                    )

                    if menu:
                        ui.delayedMessage(
                            "Telephone Operator started"
                        )
                    else:
                        ui.message(
                            "Telephone Operator started"
                        )

                except Exception:

                    log.exception(
                        "Telephone Operator: Failed to prepare Telephone Operator dialog"
                    )

                    self._updateMenuState()

                    if menu:
                        ui.delayedMessage(
                            "Telephone Operator started"
                        )
                    else:
                        ui.message(
                            "Telephone Operator started"
                        )

                return

        # ---------------------------------------------------------
        # Server did not become available.
        # ---------------------------------------------------------

        log.error(
            "Telephone Operator: Flask server did not become ready"
        )

        self._updateMenuState()

        if menu:
            ui.delayedMessage(
                "Unable to start Telephone Operator"
            )
        else:
            ui.message(
                "Unable to start Telephone Operator"
            )


    def script_startServer(self, gesture):
        """
        Start Telephone Operator. Press the gesture twice to stop Telephone Operator.        
        """

        repeatCount = scriptHandler.getLastScriptRepeatCount()

        # ---------------------------------------------------------
        # DOUBLE PRESS
        # Stop the server.
        # ---------------------------------------------------------

        if repeatCount == 1:

            log.info(
                "Telephone Operator: Double press detected - "
                "stopping server"
            )

            self._stopServer()
            return

        # ---------------------------------------------------------
        # SINGLE PRESS
        # Start the server if necessary.
        # ---------------------------------------------------------

        log.info(
            "Telephone Operator: Server start shortcut triggered"
        )

        self._startServer()


    __gestures = {
        "kb:NVDA+shift+D": "callNumber",
        "kb:NVDA+shift+T": "startServer",
    }