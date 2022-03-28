import sys
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
import screeninfo


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


def start_coffee_break_countdown():
    global timer_thread
    global stop_timer_thread
    global show_notification
    if timer_thread.is_alive():    
        stop_timer_thread = True
        show_notification = False
        time.sleep(2)
    withdraw_main_window()
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
            popup = tk.Toplevel()
            popup.title("Coffee Break")
            popup.geometry("300x100+" + str(int(screen_width / 2 - 150)) + "+" + str(int(screen_height / 2 - 50)))
            popup.resizable(False, False)
            notification_label = tk.Label(popup, text="\nTake a coffee break!", font=default_font_name + " 20")
            notification_label.pack()
            popup.tk.call('wm', 'iconphoto', popup._w, tk.PhotoImage(file=f'{DIRECTORY}/icon.png'))
            while tk.Toplevel.winfo_exists(popup):
                time.sleep(1)
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
        self.window.protocol('WM_DELETE_WINDOW', lambda: withdraw_main_window())
        self.window.title("Coffee Time")
        self.window.geometry("450x600+" + str(int(screen_width / 2 - 225)) + "+" + str(int(screen_height / 2 - 300)))
        self.window.tk.call('wm', 'iconphoto', self.window._w, tk.PhotoImage(file=f'{DIRECTORY}/icon.png'))
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
        
        
        
    window = tix.Tk()
    time_spinbox = tk.Spinbox(window, from_=1, to=60, increment=1, width=3)
    logo_frame = tk.Frame(master=window)
    logo_image = ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/proglogo.png"))
    time_frame = tk.Frame(master=window)
    time_label = tk.Label(master=time_frame, text="", font=default_font_name + ' 20')
    quote_label = tk.Label(master=time_frame, text="Focus, do what you do best.\nI will remind you when you need a rest. ;)", font=default_font)
    spinbox_value = 0
    spinbox_frame = tk.Frame(master=window,)
    spinbox_separator = tk.Label(master=window, text='\n\nCoffee break interval:', font=default_font)
    time_spinbox = tk.Spinbox(master=spinbox_frame, from_=0, to=10000,textvariable=spinbox_value, font=default_font, width=12)
    time_unit = tk.Label(master=spinbox_frame, text=' minutes', font=default_font)
    spinbox_value = 0
    start_frame = tk.Frame(master=window)
    start_button = tk.Button(master=start_frame, text='Start', command=start_coffee_break_countdown, font=default_font)
    lefttime_frame = tk.Label(master=window)
    lefttime_label = tk.Label(master=lefttime_frame, text='', font=default_font_name + ' 11')
    info_frame = tk.Frame(master=window)
    github_button = tk.Button(master=info_frame, text="GitHub", font=default_font_name + ' 11')
    sponsor_button = tk.Button(master=info_frame, text="Support", font=default_font_name + ' 11')
    quit_button = tk.Button(master=info_frame, text="Quit", font=default_font_name + ' 11')
    settings_button = tk.Button(master=info_frame, text="Settings", font=default_font_name + ' 11')



main_window = MainWindow()

def show_main_window(icon, item):
    main_window.window.after(0, main_window.window.deiconify)

def withdraw_main_window():
    main_window.window.withdraw()

def quit_coffeetime(icon, item):
    global stop_timer_thread
    global quit_everything
    stop_timer_thread = True
    quit_everything = True
    main_window.window.destroy()
    icon.visible = False    
    
def open_url(url):
    webbrowser.open(url)
    

screen_width = main_window.window.winfo_screenwidth()
screen_height = main_window.window.winfo_screenheight()
menu = (item('Show', action=show_main_window, default=True), item('Quit', action=quit_coffeetime))
icon = pystray.Icon("name", Image.open(f'{DIRECTORY}/icon.png'), "title", menu)
icon_thread = threading.Thread(target=icon.run, name="CoffeeTime Tray Icon", daemon=True)
icon_thread.start()
timer_thread = threading.Thread(target=coffee_break_countdown, name="CoffeeTime", daemon=True)


    
if __name__ == '__main__':
    main_window.launch_window()



