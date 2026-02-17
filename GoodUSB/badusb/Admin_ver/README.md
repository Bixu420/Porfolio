# GoodUsb, Badusb attack prevention program
 My first project🤫😊
## What is BadUsb attack? 🐱‍👤 -> 
A BadUSB attack is a type of cybersecurity threat where a USB device's firmware is manipulated to perform malicious actions. This type of attack takes advantage of the trust that computers typically extend to USB devices, allowing the manipulated device to execute potentially harmful commands.

## How does the program work?🤔
My program counts the intervals between keystrokes and if the average time of intervals is less than the threshold (which an admin can change) the computer locks itself preventing further keystroke injection🛑 Of course the time of the attack is logged.

## Why it works?🧐
The speed of the keystroke injection is most of the time way faster than the typing speed of a human so it's possible to differentiate an attack from normal keyboard usage. The suggested threshold is 0.017

## Aditional Feautres🏋️‍♂️
From Admin.py you can launch GUI in order to change settings for a user such as the threshold, change the user password, and whether or not you decide to save the user's public IP in log files you can also change the admin password. After clicking 'Save and launch app' admin.py launches the user version (which is responsible for monitoring keystrokes) and closes itself.

## User Version🧚‍♂️
A user is able to open the user GUI from the system tray icon and after typing the password he can stop a program for the amount of seconds he decides to in order to for example run some macros
## Security🔐
Application while running stores only 5 last keystrokes in memory. The program does not save any keystrokes or files! All passwords are hashed. The default admin login is Bombasticus34 and the password is 'Bombastic'. You can change the admin login by editing the team.json file.
