# GoodUsb, Badusb atttack prevention program
## My first project🤫😊
## What is BadUsb attack ? 🐱‍👤 -> 
A BadUSB attack is a type of cybersecurity threat where a USB device's firmware is manipulated to perform malicious actions. This type of attack takes advantage of the trust that computers typically extend to USB devices, allowing the manipulated device to execute potentially harmful commands.

## How the program works?🤔
My program counts the intervals beetween keystrokes and if the average time of intervals is less than threshold (which an admin can change) the computer locks iteslf preventing further keystroke injection🛑 Of course the time of the attack is logged.

## Why it works?🧐
The speed of the keystroke incjections is most of the time way faster than the typing speed of a human so its possible to differentiate an attatck from a normal keyboard usage. Suggested threshold is 0.017

## Aditional Feautres
From Admin.py you can launch GUI in order to change settings for a user such as the threshold,change user password and whether or not you decide to save user public ip logs. At last you can change admin password and launch user version. All passwords are hashed.

## User Version
A user is able to open user GUI from system tray icon and after typing password he can stop a program for the amount of seconds he decides to in order to for example run some macros
