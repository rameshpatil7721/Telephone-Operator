# Telephone Operator

Telephone Operator is an NVDA add-on that allows users to send a phone number from a Windows computer to a mobile phone for calling.

It is designed especially for users who work with large numbers of phone calls, such as telecallers, customer-service staff, banking staff, office users, and other professionals who frequently need to dial numbers displayed on a computer.

Instead of manually typing the phone number on the mobile phone, the user can select or focus a phone number on the computer and send it to the phone using an NVDA keyboard shortcut.

The phone displays the received number and provides a **CALL** button. The user can then press the button on the phone to place the call.

---

## Features

Telephone Operator provides the following features:

* Send a selected or focused phone number from the computer to a mobile phone.
* Works with applications such as Microsoft Excel, Microsoft Word, Notepad, web browsers, and other applications supported by NVDA.
* Supports phone numbers up to 15 digits.
* Supports Indian short service/customer-care numbers as well as longer international numbers.
* Automatically starts a local web server on the computer.
* Provides a web-based dialer interface for the phone.
* Provides a QR-code page for easier phone connection.
* Provides accessible NVDA dialogs and controls.
* Provides an NVDA Tools menu.
* Provides Start, Stop, and Instructions commands.
* Provides configurable NVDA keyboard gestures.
* Automatically closes the Telephone Operator start dialog when the server is stopped.
* Uses a temporary authentication token to prevent unauthorized requests from other devices.
* Does not require the user to manually type phone numbers on the mobile phone.

---

## How Telephone Operator Helps

Telephone Operator is useful when a phone number is already available on the computer.

For example, a telecaller may have a list of customers in Microsoft Excel.

Without Telephone Operator, the user may have to:

1. Read or copy the phone number.
2. Pick up the mobile phone.
3. Open the phone application.
4. Enter the number manually.
5. Check the number.
6. Start the call.

With Telephone Operator, the process is simplified:

1. Select or focus the phone number on the computer.
2. Press the Telephone Operator shortcut.
3. The number appears on the connected phone.
4. Press **CALL** on the phone.

This reduces manual number entry and helps avoid errors caused by typing long phone numbers.

---

## Requirements

Telephone Operator requires:

* Windows
* NVDA
* A mobile phone with a modern web browser
* The computer and mobile phone connected to the same local network

The computer and phone normally need to be connected to the same Wi-Fi network or otherwise be able to communicate over the local network.

---

## Installation

Install Telephone Operator using the `.nvda-addon` package.

1. Open the Telephone Operator `.nvda-addon` file.
2. Confirm installation when NVDA asks for permission.
3. Restart NVDA if requested.

After installation, Telephone Operator displays an information dialog containing basic usage instructions, the NVDA Tools menu location, and the default keyboard shortcuts.

Telephone Operator can then be accessed from:

**NVDA menu → Tools → Telephone Operator**

---

## First-Time Setup

After installing Telephone Operator:

1. Make sure the computer and mobile phone are connected to the same network.
2. Start Telephone Operator using **NVDA+Shift+T**.
3. NVDA will announce that Telephone Operator has started.
4. A Telephone Operator dialog will appear.
5. The dialog provides the address that must be opened on the phone.
6. The dialog also provides an option to copy the address.
7. The QR-code option can be used to open the QR-code page.
8. Open the displayed address on the mobile phone.
9. Keep the Telephone Operator page open in the phone's browser.

Once the phone is connected, it can receive phone numbers sent from the computer.

---

## Telephone Operator Address

When Telephone Operator starts, it creates a local web address.

The address is displayed in the Telephone Operator dialog.

The user can:

* Read the address using NVDA.
* Copy the address using the **Copy Phone Link** button.
* Open the QR-code page using the **Show QR Code** button.

The address can then be opened in the browser on the mobile phone.

The computer and phone must be able to communicate over the local network.

---

## Using Telephone Operator

### Step 1: Open the Telephone Operator page

On the mobile phone, open the address displayed by Telephone Operator.

Alternatively, use the QR-code page to connect more conveniently.

Keep the Telephone Operator page open in the phone's browser.

### Step 2: Select a phone number on the computer

Move to the phone number that you want to call.

The number may be located in:

* Microsoft Excel
* Microsoft Word
* Notepad
* A web page
* An edit control
* Other applications supported by NVDA

Telephone Operator attempts to use the selected or focused text.

### Step 3: Send the number

Press:

**NVDA+Shift+D**

Telephone Operator sends the detected phone number to the connected phone.

The number then appears on the Telephone Operator page on the phone.

### Step 4: Place the call

On the phone, press the **CALL** button.

The phone's normal telephone application is used to place the call.

Telephone Operator does not itself make the telephone call.

### Step 5: Continue with the next number

Return to the next phone number on the computer and repeat the process.

There is no need to manually type the number on the phone.

---

## Default Keyboard Shortcuts

| Keyboard shortcut               | Action                                                 |
| ------------------------------- | ------------------------------------------------------ |
| **NVDA+Shift+D**                | Send the selected or focused phone number to the phone |
| **NVDA+Shift+T**                | Start Telephone Operator                               |
| **NVDA+Shift+T**, pressed twice | Stop Telephone Operator                                |

The `NVDA+Shift+T` shortcut uses the same command for starting and stopping Telephone Operator.

When Telephone Operator is already running, pressing the shortcut twice within the NVDA double-press interval stops the server.

---

## Changing Keyboard Shortcuts

The default keyboard shortcuts can be changed using NVDA's Input Gestures dialog.

1. Open the NVDA menu.
2. Select **Preferences**.
3. Select **Input Gestures**.
4. Find the **Telephone Operator** category.
5. Select the command whose shortcut you want to change.
6. Add, change, or remove a keyboard gesture as required.

The default gestures are:

* **NVDA+Shift+D** — Send the selected or focused phone number.
* **NVDA+Shift+T** — Start Telephone Operator. Press the same shortcut twice within the double-press interval to stop it.

Changing a gesture does not change the underlying functionality of Telephone Operator.

This is useful if another NVDA add-on uses the same keyboard shortcut.

---

## NVDA Tools Menu

Telephone Operator is available from the NVDA Tools menu.

Open:

**NVDA menu → Tools → Telephone Operator**

The Telephone Operator submenu provides:

### Start Telephone Operator

Starts the local Telephone Operator server.

If the server is already running, the Start command is unavailable and indicates that Telephone Operator is already running.

### Stop Telephone Operator

Stops the local Telephone Operator server.

If the server is not running, the Stop command is unavailable and indicates that Telephone Operator is already stopped.

If the Telephone Operator dialog is open when the server is stopped, the dialog is automatically closed.

### Instructions

Opens the Telephone Operator instructions so that users can learn how to connect their phone and use the add-on without remembering the keyboard shortcuts.

---

## Phone Instructions

The Telephone Operator start dialog provides the essential instructions in an accessible format.

The basic process is:

1. Connect the computer and phone to the same network.
2. Open the Telephone Operator address on the phone.
3. Keep the Telephone Operator page open.
4. Select or focus a phone number on the computer.
5. Press **NVDA+Shift+D**.
6. The number appears on the phone.
7. Press **CALL** on the phone to place the call.

The dialog also provides buttons for:

* **Copy Phone Link**
* **Show QR Code**
* **Close**

The buttons can be operated using the keyboard and have accessible labels for NVDA.

---

## Multiple Phone Numbers

Telephone Operator does not automatically choose between multiple possible phone numbers when several candidates are detected in the focused text.

If multiple phone-number candidates are found, NVDA reports that multiple phone numbers were found.

In that situation:

1. Move the focus or selection to the specific phone number you want.
2. Press **NVDA+Shift+D** again.

This avoids accidentally sending an unintended number.

---

## Phone Number Detection

Telephone Operator is designed to avoid treating ordinary numeric values as telephone numbers whenever possible.

For example, ordinary values such as amounts, account numbers, or other numerical data should not automatically be treated as phone numbers merely because they contain digits.

The add-on supports phone numbers up to 15 digits.

This allows both:

* Indian telephone and customer-care numbers
* International telephone numbers

---

## Security and Authentication

Telephone Operator runs a local web server on the computer.

To prevent arbitrary devices on the local network from submitting requests to the Telephone Operator server, the server uses an authentication token.

The token is generated randomly when Telephone Operator starts.

The token is used for requests that communicate with the Telephone Operator server.

The token changes when Telephone Operator is restarted.

### Important security limitation

Telephone Operator is intended for use on a trusted local network.

The add-on does **not** provide encrypted HTTPS communication.

Do not expose the Telephone Operator server directly to the public internet.

Use Telephone Operator only on a network where you trust the connected devices.

---

## Windows Firewall

Windows may display a firewall or network-access permission dialog the first time Telephone Operator runs.

If Windows asks whether Python or NVDA should be allowed to communicate through the firewall, allow access only as appropriate for your trusted network.

For normal use, access through a **Private network** is generally appropriate when the computer and phone are connected to a trusted home or office network.

Avoid unnecessarily allowing access through **Public networks**.

If Windows Firewall blocks Telephone Operator, the mobile phone may not be able to open the Telephone Operator address.

---

## Local Network Requirement

Telephone Operator uses the local network connection between the computer and the mobile phone.

The phone does not need to be physically connected to the computer by a USB cable.

Both devices need to be able to communicate with the computer over the network.

Some corporate, guest, or public Wi-Fi networks may isolate connected devices from one another. In such networks, Telephone Operator may not work even though both devices show that they are connected to Wi-Fi.

If this happens, try a trusted private network where devices are allowed to communicate with each other.

---

## Accessibility

Telephone Operator is designed with NVDA users in mind.

The add-on uses accessible wxPython controls for its desktop dialog.

The Telephone Operator dialog provides:

* Accessible dialog title
* Accessible text controls
* Accessible buttons
* Keyboard shortcuts
* Logical tab navigation
* NVDA-readable instructions

The dialog is designed so that NVDA can read its contents when it opens.

The most important actions are also available without using the mouse.

---

## Troubleshooting

### The phone cannot open the Telephone Operator address

Check the following:

1. Make sure Telephone Operator is running.
2. Make sure the phone and computer are on the same network.
3. Check whether Windows Firewall is blocking the connection.
4. Make sure the address was entered correctly.
5. Try using the **Copy Phone Link** button instead of typing the address manually.
6. Try the QR-code option.

### The phone opens the page but does not receive numbers

Check that:

1. Telephone Operator is still running on the computer.
2. The Telephone Operator page is still open on the phone.
3. The phone and computer still have network connectivity.
4. The correct phone number is selected or focused on the computer.
5. You are using **NVDA+Shift+D** to send the number.

### NVDA says that multiple phone numbers were found

Move the selection or focus to the specific number you want to send and press:

**NVDA+Shift+D**

### Another NVDA add-on uses the same shortcut

Open:

**NVDA menu → Preferences → Input Gestures → Telephone Operator**

and assign a different keyboard gesture.

### Telephone Operator does not start

Try starting it from:

**NVDA menu → Tools → Telephone Operator → Start Telephone Operator**

If it still does not start, check the NVDA log for errors.

### Telephone Operator is already running

The Start command will indicate that Telephone Operator is already running.

You can continue using the existing Telephone Operator connection or stop it from:

**NVDA menu → Tools → Telephone Operator → Stop Telephone Operator**

---

## Stopping Telephone Operator

Telephone Operator can be stopped in two ways.

### Keyboard

Press the start/stop shortcut twice:

**NVDA+Shift+T**

### NVDA Tools menu

Open:

**NVDA menu → Tools → Telephone Operator → Stop Telephone Operator**

When the server is stopped:

* The Telephone Operator server is shut down.
* The Telephone Operator start dialog is closed if it is open.
* NVDA announces that Telephone Operator has stopped.

---

## Privacy

Telephone Operator is designed to operate locally between the computer and phone.

Phone numbers sent through Telephone Operator are transmitted through the local Telephone Operator server.

The add-on does not require a cloud service to perform the basic phone-number transfer.

Users should nevertheless use Telephone Operator only on networks they trust.

---

## Logging

Telephone Operator records important operational events in the NVDA log.

Routine diagnostic information is kept at the debug logging level where appropriate.

The add-on does not intentionally log the actual phone numbers being sent.

If troubleshooting is required, an NVDA log can help identify startup, shutdown, connection, or other operational problems.

---

## Development and Source Code

Telephone Operator is developed as an NVDA add-on.

The project source code is maintained in a Git repository.

The packaged `.nvda-addon` file is generated using the NVDA add-on build system.

---

## License

Telephone Operator is distributed under the terms of the GNU General Public License, version 2 or later.

See the included license file for the complete license terms.

---

## Feedback and Bug Reports

When reporting a problem, please provide:

* NVDA version
* Windows version
* Telephone Operator version
* Steps to reproduce the problem
* Any relevant NVDA log information
* Whether the problem occurs with the keyboard shortcut, Tools menu, or both

Do not include sensitive customer information or actual customer phone numbers in bug reports.

---

## Quick Reference

### Start

**NVDA+Shift+T**

or:

**NVDA menu → Tools → Telephone Operator → Start Telephone Operator**

### Connect phone

Open the address shown in the Telephone Operator dialog on the phone.

### Send number

Select or focus the phone number and press:

**NVDA+Shift+D**

### Call

Press **CALL** on the phone.

### Stop

Press **NVDA+Shift+T** twice, or use:

**NVDA menu → Tools → Telephone Operator → Stop Telephone Operator**

### Change shortcuts

**NVDA menu → Preferences → Input Gestures → Telephone Operator**

### Instructions

**NVDA menu → Tools → Telephone Operator → Instructions**
