import subprocess
import time
import tkinter as tk
import customtkinter
import socket
import requests
import sys
from users import UserManager
from PIL import Image, ImageTk
import signal
from Event_Logger import EventLogger
logger = EventLogger("GoodUSB")
path_to_python_exe = 'F:\python\Portfolio\.venv\Scripts\python.exe' #path to python.exe needed for admin.py to launch user version
def ignore_signal(signum, frame):
    print("Ignoring Ctrl+C")

# Set the signal handler
signal.signal(signal.SIGINT, ignore_signal)
log_path = 'log.txt' ###set up path to saving logs
def resize_image(image_path, new_width, new_height):
    
    return customtkinter.CTkImage(Image.open(image_path).resize((new_width, new_height)))
    
user_menager=UserManager()
settings_window = customtkinter.CTk()
settings_window.iconbitmap('GoodUsb2.ico')
icon1 = resize_image('eye.png', 800, 800)
icon2 = resize_image('close.png', 800, 800)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")
showip = False # argument whether the public ip should appear in logs
username=""
users=user_menager.load_user_data()
config=user_menager.load_user_config()
#print(users, config)
too_fast_threshold = 0 #minimum average time beetwen keystrokes, if the average time < threshold then the computer locks
login_window=customtkinter.CTk()
login_window.iconbitmap('GoodUsb2.ico')

def validate(): #Compare input with saved login data
    global username
    
    username=login.get()
    ##print(users[username]["password"])
    h_password=password.get()
    #print(type(h_password))
    h_password=user_menager.hash_password(h_password)
    
    #print(h_password)

    if users.get(login.get()) is None or users[username]["password"]!=h_password  :
        #print("check")
        
        login_label.configure(text="Wrong Credentials!")
    else:
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        with open (log_path, "a") as file:
            file.write ("\n")
            
            file.write (f"[{current} User {login.get()} logged in]")
        

        login_window.destroy()
        settings_window.mainloop()

login_window.geometry('500x300')
login_window.title("Enter Username and Password")

login_label=customtkinter.CTkLabel(master=login_window, text="0", text_color='#bd41d0')
login_label.place(relx=0.35, rely=0.9)
login=customtkinter.CTkEntry(master=login_window, placeholder_text='login')
login.place(relx=0.35, rely=0.35)
password=customtkinter.CTkEntry(master=login_window, placeholder_text="password", show="*")
password.place(relx=0.35, rely=0.5)
send=customtkinter.CTkButton(master=login_window, text="login",  corner_radius=32,hover=True, hover_color='#bd41d0', command=validate)
send.place(relx=0.35, rely=0.7)

def fresh(config): #read saved to fast threshhold and show ip from config file
    global too_fast_threshold, showip
    
    
    too_fast_threshold = float(config.get('threshold'))
    if config.get('showip') == 'true':
        showip = True
    else: 
        showip = False
fresh(config)
last=too_fast_threshold #last=toofast threshold before update

settings_window.geometry("500x350")
settings_window.title("Settings")
def change_handler(value):
    
    global too_fast_threshold
    too_fast_threshold = value
    text.configure(text=f"selected value={value:.4f}")    

#change admin password
def adminwpwd():
    def pwdchange():
        if login1.get() != password1.get():
            login_label1.configure(text="passwords must match!")
        elif  len(login1.get()) >26:
            login_label1.configure(text="too long password")
        elif len(login1.get()) < 8:
            login_label1.configure(text="too short password")
        else:
            named_tuple = time.localtime() # get struct_time
            current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
            pwd = user_menager.hash_password(login1.get())
            users[username]["password"] = pwd
            logger.log_warning("admin password changed", event_id=0x1008)
            with open(log_path, 'a') as file:
                file.write ("/n")
                file.write (f"[{current}]admin password change]")
                login_label1.configure(text="password changed succesfulyy")
            #print(users)
    def seepwd():
        state = login1.cget('show')
        if state == '*':

            showpwd.configure(image=icon2)
            login1.configure(show='')
            password1.configure(show='')
        else: 
            showpwd.configure(image=icon1)
            login1.configure(show='*')
            password1.configure(show='*')
    window=customtkinter.CTkToplevel(settings_window)
    window.geometry('500x350')
    login_label1=customtkinter.CTkLabel(master=window, text="0", text_color='#bd41d0')
    login_label1.place(relx=0.35, rely=0.9)
    showpwd=customtkinter.CTkButton(master=window, image=icon1, width=10, height=12, text="", command=seepwd)
    login1=customtkinter.CTkEntry(master=window, placeholder_text='password', show="*")
    login1.place(relx=0.35, rely=0.35)
    password1=customtkinter.CTkEntry(master=window, placeholder_text="retype password", show="*")
    password1.place(relx=0.35, rely=0.5)
    showpwd.place(relx=0.63, rely=0.5)
    send1=customtkinter.CTkButton(master=window, text="reset password",  corner_radius=32,hover=True, hover_color='#bd41d0', command=pwdchange)
    send1.place(relx=0.35, rely=0.7)
    window.lift()
#change User password    
def userpwd():
    def pwdchange1():
        if login1.get() != password1.get():
            login_label1.configure(text="passwords must match!")
        elif len(login1.get()) < 8:
            login_label1.configure(text="too short password")
        elif  len(login1.get()) >26:
            login_label1.configure(text="too long password")
        else:
            pwd = user_menager.hash_password(login1.get())
            config['password'] = pwd
            logger.log_warning("user password changed", event_id=0x1005)
            with open(log_path, 'a') as file:
                file.write ("/n")
                file.write ('user password changed')
                login_label1.configure(text="password changed succesfulyy")
            #print(config)
    def seepwd():
        state = login1.cget('show')
        if state == '*':

            showpwd.configure(image=icon2)
            login1.configure(show='')
            password1.configure(show='')
        else: 
            showpwd.configure(image=icon1)
            login1.configure(show='*')
            password1.configure(show='*')
    window=customtkinter.CTkToplevel(settings_window)
    window.geometry('500x350')
    login_label1=customtkinter.CTkLabel(master=window, text="0", text_color='#bd41d0')
    login_label1.place(relx=0.35, rely=0.9)
    login1=customtkinter.CTkEntry(master=window, placeholder_text='password', show="*")
    login1.place(relx=0.35, rely=0.35)
    password1=customtkinter.CTkEntry(master=window, placeholder_text="retype password", show="*")
    password1.place(relx=0.35, rely=0.5)
    send1=customtkinter.CTkButton(master=window, text="reset password",  corner_radius=32,hover=True, hover_color='#bd41d0', command=pwdchange1)
    send1.place(relx=0.35, rely=0.7)
    showpwd=customtkinter.CTkButton(master=window, image=icon1, width=10, height=12, text="", command=seepwd)
    showpwd.place(relx=0.63, rely=0.5)
    window.focus_force()

            


usermgr=customtkinter.CTkButton(master=settings_window, text="change admin password", corner_radius=32,hover=True, hover_color='#bd41d0', command=adminwpwd)
btn = customtkinter.CTkSlider(master=settings_window, from_=0.0001, to=0.1, command=change_handler)
text = customtkinter.CTkLabel(master=settings_window, text= f"Selected value: {too_fast_threshold:.4f}", font=("Arial", 20))
label= customtkinter.CTkLabel(master=settings_window, text= "Made by Bixu420", font=("Arial", 10))
btn.place(relx=0.5, rely=0.2, anchor="center") 
usermgr.place(relx=0.3, rely=0.6, anchor="center")
btn.set(too_fast_threshold)
text.place(relx = 0.5, rely=0.3, anchor="center")
label.place(relx= 0.81, rely=0.95)
usermgr1=customtkinter.CTkButton(master=settings_window, text="change user password", corner_radius=32,hover=True, hover_color='#bd41d0', command=userpwd)
usermgr1.place(relx=0.7, rely=0.6, anchor="center")
class TypingMonitor:
    
    def __init__(self):
        self.last_time = time.time()
      
        
        self.medial=1
        self.time_list = []
        self.computer_name = socket.gethostname()
    
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
    
    def log_start(self):
        global showip
        ip = self.get_location()
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logger.log_info("Admin Program started", event_id=0x1002)
        with open (log_path, "a") as file:
            file.write ("\n")
            if showip == True:
                file.write (f"[{current}]  Admin Program started hostname: {self.computer_name} ip: {ip}]")
            else:
                file.write (f"[{current}]  Admin Program started hostname: {self.computer_name}]")
    def log_end(self):
        global showip
        ip = self.get_location()
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logger.log_info("Admin Program stopped", event_id=0x1003)
        with open (log_path, "a") as file:
            
            file.write ("\n")
            if showip == True:
                file.write (f"[{current}]   Admin Program stopped hostname: {self.computer_name} ip: {ip}]")
            else:
                file.write (f"[{current}]  Admin Program stopped hostname: {self.computer_name}]")
    
    
    
#def setup(icon):
    #icon.visible = True
    
    def log_change(self):
        global too_fast_threshold
        named_tuple = time.localtime() # get struct_time
        current = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
        logger.log_info(f"threshold changed to {too_fast_threshold:.4f}", event_id=0x1004)
        with open (log_path, "a") as file:
                
            file.write ("\n")
            if showip == True:
                ip=self.get_location()
                file.write (f"[{current}]   threshold changed to {too_fast_threshold:.4f} hostname: {self.computer_name} ip: {ip}]")
            else:
                #print("writing")
                file.write (f"[{current}]   threshold changed to {too_fast_threshold:.4f} hostname: {self.computer_name}]")
   
monitor=TypingMonitor()
def switch_event():
    global showip
    #print(ipbtn.get())
    if ipbtn.get() == True:
        showip = True
        #print("ipsetting changed")
    else:
        showip = False
        #print("ipfalse")
        
def save_config():
    global showip, too_fast_threshold, config
    config['showip']=showip
    config['threshold']=too_fast_threshold
    #print("nbfaf")
    #print(config)
   

def appexit(): #exiting via UI
    
    global monitor
    global settings_window, last, config
    settings_window.destroy()
    
    save_config()
   
    user_menager.save_user_config(config)
    user_menager.save_user_data(users)
    if last !=too_fast_threshold:
        #print("changing")
        
        monitor.log_change()
    
    
    monitor = TypingMonitor()
    #run user client from admin guy
    subprocess.run([path_to_python_exe, "user.py"])
    monitor.log_end()
def kill(): #exiting via UI
    
    global monitor
    global settings_window, last
    settings_window.destroy()
    #print(users, config)
    save_config()
    user_menager.save_user_config(config)
    user_menager.save_user_data(users)
    if last !=too_fast_threshold:
        #print("changing")
        
        monitor.log_change()
    
    
    monitor = TypingMonitor()
    #print('kill')
    monitor.log_end()
    sys.exit()
    
def showip_checkbox_default_value():
    
    if showip == True:
        ipbtn.select()
    else: ipbtn.deselect()
exitbtn = customtkinter.CTkButton(master=settings_window, text="save and launch client",command=appexit, corner_radius=32,hover=True, hover_color='#bd41d0' )

ipbtn=customtkinter.CTkSwitch(master=settings_window, text="Save public ip in logs", command=switch_event, onvalue=True, offvalue=False, corner_radius =50) 
ipbtn.place(relx=0.18, rely=0.8, anchor='center')
exitbtn.place(relx= 0.5, rely=0.9, anchor='center')




        
    



settings_window.protocol("WM_DELETE_WINDOW", kill)   # default setting for pressing x on window
login_window.protocol("WM_DELETE_WINDOW", kill)

def main(): #mainloop
    global  settings_window
    
    #print(too_fast_threshold)
    # Create TypingMonitor and start listenerddadadad
    monitor = TypingMonitor()
   
    
    monitor.log_start()
    showip_checkbox_default_value()
    login_window.mainloop()
     
   

    

    
    #print("running4")
    
   
    

    #print("Exiting program...")


if __name__ == "__main__":
    main()
    
    sys.exit()
    
