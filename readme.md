# Telephone Operator for NVDA

Telephone Operator is an NVDA add-on that helps users send phone numbers from their computer directly to their smartphone without manually typing the number on the phone.

It can be useful for people who regularly work with phone numbers on a computer, including **banking and office staff, customer-service and call-centre users, data-entry operators, administrative staff, and other professionals** who handle phone numbers in Excel, Word, web pages, Notepad, or similar applications.

## Download

**[Download Telephone Operator 1.0.0](https://github.com/rameshpatil7721/Telephone-Operator/releases/download/v1.0.0/telephoneOperator-1.0.0.nvda-addon)**

For release notes and previous versions, visit the [GitHub Releases](https://github.com/rameshpatil7721/Telephone-Operator/releases) page.

## How It Works

Telephone Operator runs a small local web server on your computer.

The basic workflow is:

**Select or focus number → Send number → Number appears on phone → Verify → Press CALL**

Your phone connects to the Telephone Operator web page through the local network. You can connect by entering the displayed address in your phone's browser or by scanning the QR code.

Telephone Operator does not automatically place the call. You remain in control and verify the number before pressing **CALL** on your phone.

## Getting Started

### Requirements

You need:

- NVDA installed on your computer.
- A smartphone with a web browser.
- A local network connection between your computer and phone.

The computer and phone can be connected through the same Wi-Fi network, or you can use your phone's **personal hotspot** and connect the computer to that hotspot.

### 1. Start Telephone Operator

Open:

**NVDA menu → Tools → Telephone Operator → Start Telephone Operator**

Or use the default shortcut **(`NVDA+Alt+Z`)**.

Telephone Operator starts its local server and displays the address and QR code for connecting your phone.

**First-time use:** Windows may display a firewall or network-access prompt. If prompted, allow Telephone Operator to communicate on your **Private network** so your phone can connect to the local server.

### 2. Connect Your Phone

On your phone:

1. Scan the displayed QR code, or enter the displayed Telephone Operator address in your phone's browser.
2. Keep the Telephone Operator page open.
3. Make sure the phone and computer remain connected to the same network.

A personal hotspot can also be used. In this case, connect the computer to the phone's personal hotspot and keep the hotspot active while using Telephone Operator.

### 3. Send a Phone Number

#### In Excel

In Excel, you can use the **Send Phone Number** shortcut directly from the active cell containing the phone number.

Default shortcut: **(`NVDA+Alt+C`)**

#### In Other Applications

In applications such as Word, Notepad, web pages and other text-based applications:

1. Select the phone number you want to send.
2. Press the **Send Phone Number** shortcut.
3. The detected number is sent to your phone.
4. The number appears on the Telephone Operator page.
5. Verify the number and press **CALL** on your phone.

If multiple possible phone numbers are detected, Telephone Operator informs you instead of arbitrarily selecting one. Select the required number more precisely and try again.

### 4. Finish Using Telephone Operator

When you have finished, stop Telephone Operator from:

**NVDA menu → Tools → Telephone Operator → Stop Telephone Operator**

Or use the assigned Start/Stop shortcut **(`NVDA+Alt+Z`)**.

## Features

- Detects phone numbers from selected or focused content.
- Supports phone numbers of different lengths and is not limited to standard 10-digit Indian mobile numbers.
- Sends a detected phone number to your smartphone without manually typing it.
- Works with Excel, Word, Notepad, web pages and other suitable applications.
- Provides a QR code for convenient phone connection.
- Supports customizable NVDA keyboard shortcuts.
- Works through a local network, including a phone personal hotspot.
- Does not require a cloud account.
- Lets you verify the number on your phone before making the call.
- Maintains a short history of recently received phone numbers on the phone.

## Keyboard Shortcuts

| Action | Default shortcut |
|---|---|
| Start/Stop Telephone Operator | `NVDA+Alt+Z` |
| Send phone number | `NVDA+Alt+C` |

You can change these shortcuts from:

**NVDA menu → Preferences → Input Gestures → Telephone Operator**

Select the required command and assign your preferred shortcut.

This is useful if a shortcut conflicts with another NVDA add-on or an application.

## Privacy and Network Security

Telephone Operator communicates between your computer and phone through the local network.

- Phone numbers are sent to the local Telephone Operator server running on your computer.
- No cloud account is required.
- The add-on does not send phone numbers to an external cloud service.
- Use Telephone Operator on a trusted network.
- Always verify the number on your phone before pressing **CALL**.

The add-on itself does not place the telephone call. The normal calling mechanism of your phone is used when you press **CALL**.

## Accessibility

Telephone Operator is designed for use with NVDA and keyboard navigation.

The add-on provides accessible dialogs and controls for starting and using Telephone Operator.

Detailed instructions can be opened from:

**NVDA menu → Tools → Telephone Operator → Detailed Instructions**

The detailed instructions open in your default web browser.

## Troubleshooting

### Phone Cannot Open the Displayed Address

Check that:

- Telephone Operator is running on the computer.
- The phone and computer are connected to the same network.
- The address has been entered correctly.
- Windows Firewall is not blocking the local server.
- The phone has an active network connection.

If necessary, stop Telephone Operator and start it again.

### No Phone Number Is Detected

Make sure:

- In Excel, the active cell contains the phone number.
- In other applications, the phone number is selected.
- NVDA can access the text in the application.
- The number is clearly available to NVDA.

### Multiple Phone Numbers Are Detected

Telephone Operator may report multiple phone-number candidates instead of selecting one automatically.

Select the intended phone number more precisely and try again.

### Keyboard Shortcut Does Not Work

Open:

**NVDA menu → Preferences → Input Gestures → Telephone Operator**

Check the assigned shortcut.

If another NVDA add-on or application is using the same shortcut, assign a different shortcut.

### Phone Page Stops Responding

Check that:

- Telephone Operator is still running.
- The phone and computer are still connected to the same network.
- The Telephone Operator page is still open in the phone browser.
- Windows Firewall has not blocked the connection.

If necessary, stop Telephone Operator and start it again.

## Project and Contact

**GitHub:** [Telephone Operator on GitHub](https://github.com/rameshpatil7721/Telephone-Operator)

**Author:** Ramesh Patil

**Email:** [rameshpatil.rp019@gmail.com](mailto:rameshpatil.rp019@gmail.com)

Feedback, suggestions, and bug reports are welcome.