import ui
import logHandler
import wx
import webbrowser

log = logHandler.log


class PhoneDialerDialog(wx.Dialog):
    """Accessible dialog shown when Telephone Operator starts."""

    def __init__(self, parent, phone_url, qr_url):

        super().__init__(
            parent,
            title="Telephone Operator Started",
            size=(700, 520)
        )

        self.phone_url = phone_url
        self.qr_url = qr_url


        panel = wx.Panel(self)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # ---------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------

        title = wx.StaticText(
            panel,
            label="Telephone Operator Started"
        )

        title.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        mainSizer.Add(
            title,
            0,
            wx.ALL,
            15
        )

        # ---------------------------------------------------------
        # INTRODUCTION
        # ---------------------------------------------------------

        intro = wx.StaticText(
            panel,
            label=(
                "Telephone Operator is running on this computer.\n\n"
                "Telephone Operator helps you make calls without "
                "manually typing phone numbers on your phone.\n"
                "Select or focus a phone number on your computer and "
                "press NVDA+Shift+D or assigned shortcut. The number is sent to your phone, "
                "where you can verify it and press CALL.\n\n"
                "Use the address below to connect your phone."
            )
        )

        mainSizer.Add(
            intro,
            0,
            wx.LEFT | wx.RIGHT | wx.BOTTOM,
            15
        )

        # ---------------------------------------------------------
        # TELEPHONE OPERATOR LINK
        # ---------------------------------------------------------

        linkLabel = wx.StaticText(
            panel,
            label="Telephone Operator Address:"
        )

        mainSizer.Add(
            linkLabel,
            0,
            wx.LEFT | wx.RIGHT,
            15
        )

        self.urlText = wx.TextCtrl(
            panel,
            value=self.phone_url,
            style=wx.TE_READONLY
        )

        self.urlText.SetName(
            "Telephone Operator Address"
        )

        mainSizer.Add(
            self.urlText,
            0,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            15
        )

        # ---------------------------------------------------------
        # INSTRUCTIONS
        # ---------------------------------------------------------

        instructionsLabel = wx.StaticText(
            panel,
            label="How to use Telephone Operator for calling"
        )

        instructionsLabel.SetFont(
            wx.Font(
                11,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        mainSizer.Add(
            instructionsLabel,
            0,
            wx.LEFT | wx.RIGHT | wx.TOP,
            15
        )

        instructions = wx.StaticText(
            panel,
            label=(
                "1. Connect your computer and phone to the same "
                "Wi-Fi or network.\n\n"
                "2. Open the Telephone Operator address above on "
                "your phone, or scan the QR code.\n\n"
                "3. Keep the Telephone Operator page open in your "
                "phone's browser.\n\n"
                "4. On the computer, select or focus a phone number "
                "and press NVDA+Shift+D or assigned shortcut.\n\n"
                "5. The number will appear on your phone. Verify it "
                "and press CALL."
            )
        )

        instructions.SetName(
            "Telephone Operator Usage Instructions"
        )

        mainSizer.Add(
            instructions,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
            15
        )

        # ---------------------------------------------------------
        # BUTTONS
        # ---------------------------------------------------------

        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        self.copyButton = wx.Button(
            panel,
            label="&Copy Telephone Operator Link"
        )

        self.copyButton.SetName(
            "Copy Telephone Operator Link"
        )

        self.qrButton = wx.Button(
            panel,
            label="&Show QR Code"
        )

        self.qrButton.SetName(
            "Show QR Code"
        )

        self.closeButton = wx.Button(
            panel,
            label="C&lose"
        )

        self.closeButton.SetName(
            "Close"
        )

        buttonSizer.Add(
            self.copyButton,
            0,
            wx.RIGHT,
            10
        )

        buttonSizer.Add(
            self.qrButton,
            0,
            wx.RIGHT,
            10
        )

        buttonSizer.Add(
            self.closeButton,
            0
        )

        mainSizer.Add(
            buttonSizer,
            0,
            wx.ALIGN_CENTER | wx.ALL,
            15
        )

        panel.SetSizer(mainSizer)

        # ---------------------------------------------------------
        # BUTTON EVENTS
        # ---------------------------------------------------------

        self.copyButton.Bind(
            wx.EVT_BUTTON,
            self.onCopy
        )

        self.qrButton.Bind(
            wx.EVT_BUTTON,
            self.onShowQR
        )

        self.closeButton.Bind(
            wx.EVT_BUTTON,
            self.onClose
        )

        self.Bind(
            wx.EVT_CHAR_HOOK,
            self.onKeyPress
        )

        # ---------------------------------------------------------
        # INITIAL FOCUS
        # ---------------------------------------------------------

        # Keep the initial focus on Copy Telephone Operator Link.
        self.copyButton.SetFocus()

        self.Centre()


    # -------------------------------------------------------------
    # COPY TELEPHONE OPERATOR LINK
    # -------------------------------------------------------------

    def onCopy(self, event):

        if wx.TheClipboard.Open():

            wx.TheClipboard.SetData(
                wx.TextDataObject(self.phone_url)
            )

            wx.TheClipboard.Close()

            ui.message(
                "Telephone Operator link copied to clipboard"
            )

        else:

            ui.message(
                "Unable to copy Telephone Operator link"
            )

    # -------------------------------------------------------------
    # SHOW QR CODE
    # -------------------------------------------------------------

    def onShowQR(self, event):

        try:

            webbrowser.open(self.qr_url)

            ui.message(
                "QR code opened in browser"
            )

        except Exception:

            log.exception(
                "Telephone Operator: Unable to open QR code"
            )

            ui.message(
                "Unable to open QR code"
            )

    # -------------------------------------------------------------
    # CLOSE
    # -------------------------------------------------------------

    def onClose(self, event):

        self.EndModal(wx.ID_CLOSE)

    # -------------------------------------------------------------
    # KEYBOARD SHORTCUTS
    # -------------------------------------------------------------

    def onKeyPress(self, event):

        key = event.GetKeyCode()

        # Escape = Close
        if key == wx.WXK_ESCAPE:

            self.EndModal(wx.ID_CLOSE)
            return

        # Alt+C = Copy Telephone Operator Link
        if event.AltDown() and key in (ord("C"), ord("c")):

            self.onCopy(None)
            return

        # Alt+Q = Show QR Code
        if event.AltDown() and key in (ord("Q"), ord("q")):

            self.onShowQR(None)
            return

        # Alt+L = Close
        if event.AltDown() and key in (ord("L"), ord("l")):

            self.EndModal(wx.ID_CLOSE)
            return

        event.Skip()


class InstructionsDialog(wx.Dialog):
    """Display instructions for using Telephone Operator."""

    def __init__(self, parent):

        super().__init__(
            parent,
            title="Telephone Operator Instructions",
            size=(700, 600)
        )

        panel = wx.Panel(self)

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # ---------------------------------------------------------
        # TITLE
        # ---------------------------------------------------------

        title = wx.StaticText(
            panel,
            label="Telephone Operator Instructions"
        )

        title.SetFont(
            wx.Font(
                14,
                wx.FONTFAMILY_DEFAULT,
                wx.FONTSTYLE_NORMAL,
                wx.FONTWEIGHT_BOLD
            )
        )

        mainSizer.Add(
            title,
            0,
            wx.ALL,
            15
        )

        # ---------------------------------------------------------
        # INSTRUCTIONS
        # ---------------------------------------------------------

        instructions = wx.TextCtrl(
            panel,
            value=(
                "1. Start Telephone Operator from the NVDA Tools "
                "menu or by using the assigned shortcut.\n\n"

                "2. Make sure your computer and phone are connected "
                "to the same Wi-Fi or network.\n\n"

                "3. On your phone, open the Telephone Operator address "
                "shown by the add-on. You can also scan the QR code.\n\n"

                "4. Keep the Telephone Operator page open in your "
                "phone's browser.\n\n"

                "5. On the computer, select or focus the phone number "
                "you want to call.\n\n"

                "6. Press NVDA+Shift+D or assigned shortcut to send the number to your phone.\n\n"

                "7. The number will appear on the Telephone Operator "
                "page on your phone.\n\n"

                "8. Verify the number and press the CALL button "
                "on your phone.\n\n"

                "9. When you have finished using Telephone Operator, "
                "stop it from the NVDA Tools menu or by using "
                "the assigned shortcut."
            ),
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_WORDWRAP
        )

        instructions.SetName(
            "Telephone Operator Instructions"
        )

        mainSizer.Add(
            instructions,
            1,
            wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM,
            15
        )

        # ---------------------------------------------------------
        # CLOSE BUTTON
        # ---------------------------------------------------------

        closeButton = wx.Button(
            panel,
            label="C&lose"
        )

        closeButton.SetName(
            "Close"
        )

        mainSizer.Add(
            closeButton,
            0,
            wx.ALIGN_CENTER | wx.ALL,
            15
        )

        panel.SetSizer(mainSizer)

        # ---------------------------------------------------------
        # EVENTS
        # ---------------------------------------------------------

        closeButton.Bind(
            wx.EVT_BUTTON,
            self.onClose
        )

        self.Bind(
            wx.EVT_CHAR_HOOK,
            self.onKeyPress
        )

        # ---------------------------------------------------------
        # INITIAL FOCUS
        # ---------------------------------------------------------

        instructions.SetFocus()

        self.Centre()

    def onClose(self, event):

        self.EndModal(wx.ID_CLOSE)

    def onKeyPress(self, event):

        key = event.GetKeyCode()

        if key == wx.WXK_ESCAPE:

            self.EndModal(wx.ID_CLOSE)
            return

        if event.AltDown() and key in (ord("L"), ord("l")):

            self.EndModal(wx.ID_CLOSE)
            return

        event.Skip()