from pynput import keyboard
from PIL import Image
import pystray
from pystray import MenuItem as item
import customtkinter
import time
import ctypes
import socket
import requests
import sys
from users import UserManager
import signal
import wmi
import logging
from logging.handlers import NTEventLogHandler
import win32evtlogutil
import os
from Event_Logger import EventLogger
logger = EventLogger("GoodUSB")
# Signal handler function
def ignore_signal(signum, frame):
    print("Ignoring Ctrl+C")

# Set the signal handler
signal.signal(signal.SIGINT, ignore_signal)
badpass = 0
# Your main code
log_path="log.txt" ##set file for logging events
user_menager=UserManager()
config = user_menager.load_user_config()


login_window=customtkinter.CTk()
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
login_window.geometry('500x300')
login_window.iconbitmap('GoodUsb2.ico')
login_window.title("Enter Username and Password")
def validate():
    global Running, badpass
    named_tuple = time.localtime() # get struct_time
    current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    key=config.get('password')
    pwd=user_menager.hash_password(password.get())
    
    if pwd != key or not duration.get().isdigit() or duration.get() =="":
       
        
        badpass+=1
        if badpass ==3:
            logger.log_warning("User typed wrong password over 3 times", event_id=0x1007)
            with open (log_path, "a") as file:
                file.write ("\n")
            
                file.write (f"[{current}] User typed wrong pass 3 times!! ]")
        #print("check")
        password.delete(0, 'end')
        login_label.configure(text="Wrong Credentials!")
    

    else:
        badpass=0
        login_label.configure(text=f"waiting {duration.get()} seconds")
        amount=int(duration.get())
        password.delete(0, 'end')
        duration.delete(0, 'end')
        
        Running=False
        login_window.after(amount*1000, val)
        logger.log_info(f" User suspended program [{amount}]", event_id=0x1001)
        with open (log_path, "a") as file:
            file.write ("\n")
            
            file.write (f"[{current}] User suspended program [{amount}]")
        #wait(amount)
        
        
        
        



login_label=customtkinter.CTkLabel(master=login_window, text='', text_color='#bd41d0')
login_label.place(relx=0.35, rely=0.9)
duration=customtkinter.CTkEntry(master=login_window, placeholder_text='duration in sec', )
duration.place(relx=0.35, rely=0.35)
password=customtkinter.CTkEntry(master=login_window, placeholder_text="password", show="*")
password.place(relx=0.35, rely=0.5)
send=customtkinter.CTkButton(master=login_window, text="login",  corner_radius=32,hover=True, hover_color='#bd41d0', command=validate)
send.place(relx=0.35, rely=0.7)

Running = True
showip = False # argument whether the public ip should appear in logs


too_fast_threshold = 0 #minimum average time beetwen keystrokes, if the average time < threshold then the computer locks

def fresh(config): #read saved to fast threshhold and show ip from config file
    global too_fast_threshold, showip
   
    
    
    too_fast_threshold = float(config.get('threshold'))
    showip = config.get('showip')
    #print(showip)

fresh(config)
last=too_fast_threshold #last=toofast threshold before update

def val():
    global Running, login_window
    Running=True
    login_label.configure(text="Finished waiting")


class TypingMonitor:
    
    def __init__(self):
        self.last_time = time.time()
        self.listener = keyboard.Listener(on_press=self.on_press)
        
        self.medial=1
        self.time_list = []
        self.computer_name = socket.gethostname()
    def list_keyboards(self):
        c = wmi.WMI()
        self.keyboards = c.Win32_Keyboard()
        self.keyboard_amount=len(self.keyboards)
    def get_location(self):
        try:
            response = requests.get('https://ipinfo.io/')
            if response.status_code == 200:
                data = response.json()
                country = data.get('ip', 'Not available')
                return country
            else:
                return "Could not fetch location data"
        except requests.RequestException:
            return "Request failed"
    def check(self):
        
        self.medial = sum(self.time_list[-6:]) / 6
        self.time_list = []
        return self.medial
    def log_start(self):
        global showip
        ip = self.get_location()
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logger.log_info(f"Program started", event_id=0x1000)
        with open (log_path, "a") as file:
            file.write ("\n")
            if showip == True:
                file.write (f"[{current}]   Program started hostname: {self.computer_name} ip: {ip}]")
            else:
                file.write (f"[{current}]   Program started hostname: {self.computer_name}]")
    def log_end(self):
        global showip
        ip = self.get_location()
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logger.log_warning(f"Program stopped", event_id=0x1006)
        with open (log_path, "a") as file:
            
            file.write ("\n")
            if showip == True:
                file.write (f"[{current}]   Program stopped hostname: {self.computer_name} ip: {ip}]")
            else:
                file.write (f"[{current}]   Program stopped hostname: {self.computer_name}]")
    def log_alert(self):
        ip = self.get_location()
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logger.log_error(f"ATTACK DETECTED", event_id=0x1009)
        with open (log_path, "a") as file:
            
            file.write ("\n")
            if showip ==True:
                file.write (f"[{current}]   ATTACK DETECTED hostname: {self.computer_name} ip: {ip}]")
            else: file.write (f"[{current}]   ATTACK DETECTED hostname: {self.computer_name}]")
    
    
    def on_press(self, key):
        if isinstance(key, keyboard.Key):
            return
        if key == keyboard.Key.backspace:
            return
        global too_fast_threshold, Running
        current_time = time.time()
        interval = current_time - self.last_time
        self.last_time = current_time
        self.time_list.append(interval)  # Update time_list with the interval
        if len(self.time_list) >= 6:
            self.check()
            print(f"self medial: {self.medial}")

        if self.medial < too_fast_threshold and Running ==True:
            #print(f"Possible BadUSB attack detected! Typing too fast: {self.medial:.4f}]")
            self.medial=1
            self.lock_computer()
            self.log_alert()
            self.medial=1
            
            

        #try:
        print(f"Key {key.char} pressed, interval: {interval:.4f} seconds] {Running}, {self.medial}")  
        #except AttributeError:
            #pass  # Handle special keys here if needed

    def lock_computer(self):
        ctypes.windll.user32.LockWorkStation()

    def start(self):
        self.listener.start()
        self.listener.join()
#def setup(icon):
    #icon.visible = True
    
    

        

def image(): #get icon image
    try:
        icon_image = Image.open("GoodUsb2.png")  # Ensure the image path is correct
        return icon_image
    except FileNotFoundError:
        #print("Icon image not found. Exiting.")
        sys.exit(1)   
def hide():
    global login_window
    #print('HID')
    login_window.withdraw()
    starti()
def ui(icon):
    global login_window
    icon.stop()
    #login_label.configure(text='')
    login_window.deiconify()      
def wait(amount):
    
    global Running, login_window
    login_window.withdraw()
    
    #print('waitin')
    Running = False
    time.sleep(amount)
    Running = True
    starti()
 

def starti(): #star tray 
    menu = (item('Suspend',ui),)
    icon = pystray.Icon("lol.jpg", image(), "My System Tray Icon", menu)
    icon.run()     
    
    
   


   
    
    
  

    
    

login_window.protocol("WM_DELETE_WINDOW", hide)
def main(): #mainloop
    global  listener, monitor, login_window
    
    #print(too_fast_threshold)
    # Create TypingMonitor and start listenerddadadad
    monitor = TypingMonitor()
    listener = keyboard.Listener(on_press=monitor.on_press)
    listener.start()
    monitor.log_start()
    
    login_window.mainloop()
    login_window.withdraw()
    
    #starti()


    

    
    #print("running4")
    
    # Main loop
    

    #print("Exiting program...")


if __name__ == "__main__":
    main()
