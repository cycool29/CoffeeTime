import configparser
import plyer
import threading
import os
os.environ['PYSTRAY_BACKEND'] = 'gtk'
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import ImageTk, Image
from tkinter import tix
import tkinter as tk
import datetime
import pystray
from pystray import MenuItem as item
import time
import webbrowser
# from settings import *

if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")
stop_timer_thread = False
quit_everything = False
show_notification = True
font = Gtk.Settings.get_default().get_property("gtk-font-name")
default_font_name = font.split(',')[0].replace(' ', '')
default_font_size = font[-2:]
default_font = default_font_name + ' ' + default_font_size

config = configparser.ConfigParser()
config.read(DIRECTORY + '/configurations.ini')
coffee_break_interval = config['CoffeeTime']['coffee_break_interval']
coffee_break_message = config['CoffeeTime']['coffee_break_message']
coffee_break_sound = config['CoffeeTime']['coffee_break_sound']
coffee_or_water = config['CoffeeTime']['coffee_or_water']
ramdom_daily_quotes = config['CoffeeTime']['ramdom_daily_quotes']

def open_subwindow(window):
    x = window()
    cycool29_is_very_cool = x.launch_window()

def start_coffee_break_countdown():
    global timer_thread
    global stop_timer_thread
    global show_notification
    if timer_thread.is_alive():    
        stop_timer_thread = True
        show_notification = False
        time.sleep(2)
    withdraw_window(main_window)
    stop_timer_thread = False
    show_notification = True
    timer_thread = threading.Thread(target=coffee_break_countdown, name="CoffeeTime", daemon=True)
    timer_thread.start()

def coffee_break_countdown():
    global stop_timer_thread
    countdown_time_seconds = int(main_window.time_spinbox.get())*60 # minutes to seconds 
    original_countdown_time = countdown_time_seconds
    current_time_seconds = int(datetime.datetime.now().strftime("%H"))*3600 + int(datetime.datetime.now().strftime("%M"))*60 # hour to seconds + minutes to seconds
    next_break_time_seconds = current_time_seconds + countdown_time_seconds
    next_break_time_interval_seconds  = next_break_time_seconds - current_time_seconds
    next_break_time_interval_user = next_break_time_interval_seconds / 60
    
    if next_break_time_interval_user == 1:
        main_window.lefttime_label['text'] = "\nYour next coffee break is at a minute later."
        main_window.lefttime_label.pack()
    elif next_break_time_interval_user > 1:
        main_window.lefttime_label['text'] = "\nYour next coffee break is at " + str(next_break_time_interval_user).split('.')[0] + " minutes later."
        main_window.lefttime_label.pack()
    elif next_break_time_interval_user < 1:
        main_window.lefttime_label['text'] = "\nYour next coffee break is at less than a minute later."
        main_window.lefttime_label.pack()

    while True:
        if stop_timer_thread == True:
            break
        
        while countdown_time_seconds > 0:
            try:
                print(countdown_time_seconds)
                current_time_seconds = int(datetime.datetime.now().strftime("%H"))*3600 + int(datetime.datetime.now().strftime("%M"))*60
                next_break_time_seconds = current_time_seconds + countdown_time_seconds
                next_break_time_interval_seconds  = next_break_time_seconds - current_time_seconds
                next_break_time_interval_user = next_break_time_interval_seconds / 60
                
                if next_break_time_interval_user == 1:
                    main_window.lefttime_label['text'] = "\nYour next coffee break is at a minute later."
                    main_window.lefttime_label.pack()
                elif next_break_time_interval_user > 1:
                    main_window.lefttime_label['text'] = "\nYour next coffee break is at " + str(next_break_time_interval_user).split('.')[0] + " minutes later."
                    main_window.lefttime_label.pack()
                elif next_break_time_interval_user < 1:
                    main_window.lefttime_label['text'] = "\nYour next coffee break is at less than a minute later."
                    main_window.lefttime_label.pack()
                
                countdown_time_seconds -= 1
                time.sleep(1)
            
            except:
                stop_timer_thread = True
                break
            if stop_timer_thread == True:
                break

        if show_notification == True:
            open_subwindow(NotificationWindow)
            countdown_time_seconds = original_countdown_time
        else:
            stop_timer_thread = True

class MainWindow:                
    def update_current_time_seconds(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        if quit_everything != True:
            self.time_label['text'] = "It's " + current_time + ' now.\n'
        self.window.after(1, self.update_current_time_seconds)

    def launch_window(self):
        self.window.protocol('WM_DELETE_WINDOW', withdraw_window(self))
        self.window.title("Coffee Time")
        self.window.geometry("450x600+" + str(int(screen_width / 2 - 225)) + "+" + str(int(screen_height / 2 - 300)))
        self.window.iconphoto(True, ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/icon.png")))
        self.window.deiconify()
        self.time_spinbox.pack()
        self.start_button.pack()

        # Logo frame
        tk.Label(master=self.logo_frame, image=self.logo_image).pack()
        self.logo_frame.pack()


        # Text frame
        self.time_label.pack()
        self.quote_label.pack()
        self.time_frame.pack()


        # Spinbox frame
        self.spinbox_separator.pack()
        self.time_spinbox.pack(side=tk.LEFT)
        self.time_unit.pack(side=tk.RIGHT)
        self.spinbox_frame.pack()


        # Start from spinbox
        self.start_button.pack(side=tk.BOTTOM, pady=10)
        self.start_frame.pack()


        # Left time
        main_window.lefttime_label.pack()
        self.lefttime_frame.pack()

        # Info frame
        self.github_button.bind(
            "<Button-1>", lambda e: open_url("https://github.com/cycool29/coffeetime"))
        self.sponsor_button.bind(
            "<Button-1>", lambda e: open_url("https://buymeacoffee.com/cycool29"))
        self.quit_button.bind("<Button-1>", quit_coffeetime)
        self.info_frame.pack(side="bottom",)
        self.github_button.pack(side="left", padx=5, pady=5)
        self.quit_button.pack(side="right", padx=5, pady=5)
        self.settings_button.pack(side="right", padx=5, pady=5)
        self.sponsor_button.pack(side="right", padx=5, pady=5)
        tix.Balloon(self.window).bind_widget(self.github_button,
                                        balloonmsg="View CoffeeTime GitHub page.")
        tix.Balloon(self.window).bind_widget(self.sponsor_button,
                                        balloonmsg="Buy cycool29 a coffee.")
        tix.Balloon(self.window).bind_widget(self.quit_button, balloonmsg="Quit CoffeeTime.")
        tix.Balloon(self.window).bind_widget(self.settings_button, balloonmsg="Change CoffeeTime settings.")

        self.update_current_time_seconds()

        self.window.mainloop()
        
        
    def __init__(self) -> None:
        self.window = tix.Tk()
        self.time_spinbox = tk.Spinbox(self.window, from_=1, to=60, increment=1, width=3)
        self.logo_frame = tk.Frame(master=self.window)
        self.logo_image = ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/proglogo.png"))
        self.time_frame = tk.Frame(master=self.window)
        self.time_label = tk.Label(master=self.time_frame, text="", font=default_font_name + ' 20')
        self.quote_label = tk.Label(master=self.time_frame, text="Focus, do what you do best.\nI will remind you when you need a rest. ;)", font=default_font)
        self.spinbox_value = 30
        self.spinbox_frame = tk.Frame(master=self.window,)
        self.spinbox_separator = tk.Label(master=self.window, text='\n\nCoffee break interval:', font=default_font)
        self.time_spinbox = tk.Spinbox(master=self.spinbox_frame, from_=0, to=10000, font=default_font, width=12, textvariable=self.spinbox_value)
        self.time_unit = tk.Label(master=self.spinbox_frame, text=' minutes', font=default_font)
        self.spinbox_value = 0
        self.start_frame = tk.Frame(master=self.window)
        self.start_button = tk.Button(master=self.start_frame, text='Start', command=start_coffee_break_countdown, font=default_font)
        self.lefttime_frame = tk.Label(master=self.window)
        self.lefttime_label = tk.Label(master=self.lefttime_frame, text='', font=default_font_name + ' 11')
        self.info_frame = tk.Frame(master=self.window)
        self.github_button = tk.Button(master=self.info_frame, text="GitHub", font=default_font_name + ' 11')
        self.sponsor_button = tk.Button(master=self.info_frame, text="Support", font=default_font_name + ' 11')
        self.quit_button = tk.Button(master=self.info_frame, text="Quit", font=default_font_name + ' 11')
        self.settings_button = tk.Button(master=self.info_frame, text="Settings", font=default_font_name + ' 11', command=lambda:open_subwindow(SettingsWindow))

# default coffee break interval
# default notification message
# default notification sound
# notiification sound?
# water or coffee
# random daily quote
# theme

class SettingsWindow:
    def launch_window(self):
        self.settings_window.geometry("450x650+" + str(int(screen_width / 2 - 225)) + "+" + str(int(screen_height / 2 - 325)))
        self.settings_window.title('CoffeeTime Settings')
        tk.Label(master=self.settings_title_frame, image=ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/proglogo.png"))).pack()
        self.settings_title_label.pack()
        self.settings_title_frame.pack()
        self.coffee_break_interval_label.pack()
        self.coffee_break_interval_spinbox.pack()
        self.coffee_break_interval_frame.pack()
        self.coffee_break_message_label.pack()
        self.coffee_break_message_entry.pack()
        self.coffee_break_message_frame.pack()
        self.coffee_break_sound_label.pack()
        self.coffee_break_sound_button.pack()
        self.coffee_break_sound_frame.pack()
        self.theme_label.pack()
        self.theme_spinbox.pack()
        self.theme_frame.pack()
        self.settings_window.mainloop()
            
    def update_config(self):
        config['CoffeeTime']['coffee_break_interval'] = self.coffee_break_interval_spinbox.get()
        config['CoffeeTime']['coffee_break_message'] = self.coffee_break_message_entry.get()
        config['CoffeeTime']['coffee_break_sound'] = self.coffee_break_sound
        config['CoffeeTime']['theme'] = self.theme_spinbox.get()
        
        with open('configurations.ini', 'w') as configfile:
            config.write(configfile)
        
    def choose_sound_file(self):
        self.coffee_break_sound = plyer.filechooser.open_file(filters=["*mp3", "*ogg", "*aac"], title='Choose a sound file', icon=f'{DIRECTORY}/icon.png')[0]
        if os.path.isfile(self.coffee_break_sound):
            self.update_config()

    def __init__(self) -> None:
        self.settings_window = tk.Toplevel()
        self.coffee_break_interval_stringvar = tk.StringVar(value=coffee_break_interval)
        self.coffee_break_message_stringvar = tk.StringVar(value=coffee_break_message)
        self.theme_stringvar = tk.StringVar(value='light')
        
        self.settings_title_frame = tk.Frame(master=self.settings_window)
        self.settings_title_label = tk.Label(master=self.settings_title_frame, text='Settings\n', font=default_font_name + ' 25')

        self.coffee_break_interval_frame = tk.Frame(master=self.settings_window)
        self.coffee_break_interval_label = tk.Label(master=self.coffee_break_interval_frame, text='Coffee break interval:', font=default_font)
        self.coffee_break_interval_spinbox = tk.Spinbox(master=self.coffee_break_interval_frame, from_=1, to=10000, textvariable=self.coffee_break_interval_stringvar, font=default_font, command=self.update_config)

        self.coffee_break_message_frame = tk.Frame(master=self.settings_window)
        self.coffee_break_message_label = tk.Label(master=self.coffee_break_message_frame, text='\nCoffee break message:', font=default_font)
        self.coffee_break_message_entry = tk.Entry(master=self.coffee_break_message_frame, textvariable=self.coffee_break_message_stringvar, font=default_font, validatecommand=self.update_config)
        
        self.coffee_break_sound_frame = tk.Frame(master=self.settings_window)
        self.coffee_break_sound_label = tk.Label(master=self.coffee_break_sound_frame, text='\nSelect a coffee break sound effect:', font=default_font)
        self.coffee_break_sound_button = tk.Button(master=self.coffee_break_sound_frame, text='Select file', font=default_font, command=self.choose_sound_file)

        self.theme_frame = tk.Frame(master=self.settings_window)
        self.theme_label = tk.Label(master=self.theme_frame, text='\nSelect a theme:', font=default_font)
        self.theme_spinbox = tk.Spinbox(master=self.theme_frame, textvariable=self.theme_stringvar, font=default_font, command=self.update_config, values=['Light', 'Dark'], wrap=True)



class NotificationWindow:
    def __init__(self) -> None:
        self.notification_window = tk.Toplevel()
        self.notification_label = tk.Label(self.notification_window, text="\nTake a coffee break!", font=default_font_name + " 20")
        self.logo_image = ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/icon.png"))
    
    def launch_window(self):
        self.notification_window.attributes('-topmost', 'true')
        self.notification_window.iconphoto(False, self.logo_image)
        self.notification_window.title("Coffee Break!")
        self.notification_window.geometry("300x100+" + str(int(screen_width / 2 - 150)) + "+" + str(int(screen_height / 2 - 50)))
        self.notification_window.resizable(False, False)
        self.notification_label.pack()
        while tk.Toplevel.winfo_exists(self.notification_window):
            self.notification_window.geometry("300x100+" + str(int(screen_width / 2 - 150)) + "+" + str(int(screen_height / 2 - 50)))
            self.notification_window.update()
            time.sleep(1)
            print('waiting')



main_window = MainWindow()

def show_main_window(icon, item):
    main_window.window.after(0, main_window.window.deiconify)

def withdraw_window(window=main_window):
    window.window.withdraw()  
    
def open_url(url):
    webbrowser.open(url)

def quit_coffeetime(icon, item=None):
    global stop_timer_thread
    global quit_everything
    stop_timer_thread = True
    quit_everything = True
    main_window.window.destroy()
    icon.visible = False  
    
screen_width = main_window.window.winfo_screenwidth()
screen_height = main_window.window.winfo_screenheight()
menu = (item('Show', action=show_main_window, default=True), item('Quit', action=quit_coffeetime))
icon = pystray.Icon("name", Image.open(f'{DIRECTORY}/icon.png'), "title", menu)
icon_thread = threading.Thread(target=icon.run, name="CoffeeTime Tray Icon", daemon=True)
icon_thread.start()
timer_thread = threading.Thread(target=coffee_break_countdown, name="CoffeeTime", daemon=True)


    
if __name__ == '__main__':
    main_window.launch_window()



