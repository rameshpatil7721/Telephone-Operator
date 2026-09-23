import wx
import gui


def onInstall():
    message = (
        "Telephone Operator has been successfully installed.\n\n"
        "To use Telephone Operator, open the NVDA menu, then go to "
        "Tools > Telephone Operator. From there you can start or stop "
        "Telephone Operator and open the instructions.First-time use: Windows may display a firewall or network-access prompt. If prompted, allow Telephone Operator to communicate on your Private network \n\n"
        "Default keyboard shortcuts:\n"
        "NVDA+Alt+C: Send the selected or focused phone number.\n"
        "NVDA+Alt+Z: Start Telephone Operator. Press twice to stop it.\n\n"
        "You can change these shortcuts from "
        "NVDA > Preferences > Input Gestures > Telephone Operator."
    )

    gui.messageBox(
        message,
        "Telephone Operator Installed",
        wx.OK | wx.ICON_INFORMATION
    )