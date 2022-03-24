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

def update_current_time_seconds():
    currentTime = datetime.datetime.now().strftime("%H:%M")
    if quit_everything != True:
        time_label['text'] = "It's " + currentTime + ' now.\n'
    window.after(1, update_current_time_seconds)

def quit_window(icon, item):
    global stop_timer_thread
    global quit_everything
    stop_timer_thread = True
    quit_everything = True
    window.destroy()
    icon.destroy()
    
def show_window(icon, item):
    window.after(0, window.deiconify)

def withdraw_window():
    window.withdraw()

def open_url(url):
    webbrowser.open(url)

def start_coffee_break_countdown():
    global timer_thread
    global stop_timer_thread
    global show_notification
    if timer_thread.is_alive():    
        stop_timer_thread = True
        show_notification = False
        time.sleep(2)
    withdraw_window()
    timer_thread = threading.Thread(target=coffee_break_countdown, name="CoffeeTime", daemon=True)
    stop_timer_thread = False
    timer_thread.start()

def coffee_break_countdown():
    global stop_timer_thread
    countdown_time_seconds = int(time_spinbox.get())*60 # minutes to seconds 
    original_countdown_time = countdown_time_seconds
    current_time_seconds = int(datetime.datetime.now().strftime("%H"))*3600 + int(datetime.datetime.now().strftime("%M"))*60 # hour to seconds + minutes to seconds
    next_break_time_seconds = current_time_seconds + countdown_time_seconds
    next_break_time_interval_seconds  = next_break_time_seconds - current_time_seconds
    next_break_time_interval_user = next_break_time_interval_seconds / 60
    
    if next_break_time_interval_user == 1:
        lefttime_label['text'] = "\nYour next coffee break is at a minute later."
        lefttime_label.pack()
    elif next_break_time_interval_user > 1:
        lefttime_label['text'] = "\nYour next coffee break is at " + str(next_break_time_interval_user).split('.')[0] + " minutes later."
        lefttime_label.pack()
    elif next_break_time_interval_user < 1:
        lefttime_label['text'] = "\nYour next coffee break is at less than a minute later."
        lefttime_label.pack()

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
                    lefttime_label['text'] = "\nYour next coffee break is at a minute later."
                    lefttime_label.pack()
                elif next_break_time_interval_user > 1:
                    lefttime_label['text'] = "\nYour next coffee break is at " + str(next_break_time_interval_user).split('.')[0] + " minutes later."
                    lefttime_label.pack()
                elif next_break_time_interval_user < 1:
                    lefttime_label['text'] = "\nYour next coffee break is at less than a minute later."
                    lefttime_label.pack()
                
                countdown_time_seconds -= 1
                time.sleep(1)
            
            except:
                stop_timer_thread = True
                break
            if stop_timer_thread == True:
                break

                
        popup = tk.Toplevel()
        popup_width = int(popup.winfo_screenwidth() / 2 - 150)
        popup_height = int(popup.winfo_screenheight() / 2 - 50)
        popup.title("Coffee Break")
        popup.geometry("300x100+" + str(popup_width) + "+" + str(popup_height))
        popup.resizable(False, False)
        notification_label = tk.Label(popup, text="\nTake a coffee break!", font=default_font_name + " 20")
        notification_label.pack()
        popup.tk.call('wm', 'iconphoto', popup._w, tk.PhotoImage(file=f'{DIRECTORY}/icon.png'))
        while tk.Toplevel.winfo_exists(popup):
            time.sleep(1)
        countdown_time_seconds = original_countdown_time



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
menu = (item('Show', show_window, default=True), item('Quit', quit_window))
icon = pystray.Icon("name", Image.open(f'{DIRECTORY}/icon.png'), "title", menu)
icon_thread = threading.Thread(target=icon.run, daemon=True, name="CoffeeTime Tray Icon")
icon_thread.start()
timer_thread = threading.Thread(target=coffee_break_countdown, name="CoffeeTime", daemon=True)


# Create window
window = tix.Tk()
icon_photo = tk.PhotoImage(file=f'{DIRECTORY}/icon.png')
window.geometry("450x750+500+100")
window.title('CoffeeTime')
window.iconphoto(False, icon_photo)
window.protocol('WM_DELETE_WINDOW', withdraw_window)


# Logo frame
logo_frame = tk.Frame(master=window)
logo_image = ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/proglogo.png"))
tk.Label(master=logo_frame, image=logo_image).pack()
logo_frame.pack()


# Text frame
time_frame = tk.Frame(master=window)
time_label = tk.Label(master=time_frame, text="",
                      font=default_font_name + ' 20')
quote_label = tk.Label(
    master=time_frame, text="Focus, do what you do best.\nI will remind you when you need a rest. ;)", font=default_font)
time_label.pack()
quote_label.pack()
time_frame.pack()


# Spinbox frame
spinbox_value = 0
spinbox_frame = tk.Frame(master=window,)
spinbox_separator = tk.Label(
    master=spinbox_frame, text='\n\nCoffee break interval:', font=default_font)
time_spinbox = tk.Spinbox(master=spinbox_frame, from_=0, to=10000,
                          textvariable=spinbox_value, font=default_font, width=10)
time_unit = tk.Label(master=spinbox_frame, text=' minutes', font=default_font)
spinbox_separator.pack()
time_spinbox.pack(side=tk.LEFT)
time_unit.pack(side=tk.RIGHT)
spinbox_frame.pack()


# Start from spinbox
start_frame = tk.Frame(master=window)
start_button = tk.Button(master=start_frame, text='Start', command=start_coffee_break_countdown, font=default_font)
start_button.pack(side=tk.BOTTOM, pady=10)
start_frame.pack()


# Left time
lefttime_frame = tk.Label(master=window)
lefttime_label = tk.Label(master=lefttime_frame, text='', font=default_font_name + ' 11')
lefttime_label.pack()
lefttime_frame.pack()

# Info frame
info_frame = tk.Frame(master=window)
github_button = tk.Button(master=info_frame, text="GitHub", font=default_font_name + ' 11')
sponsor_button = tk.Button(
    master=info_frame, text="Support", font=default_font_name + ' 11')
quit_button = tk.Button(master=info_frame, text="Quit", font=default_font_name + ' 11')
settings_button = tk.Button(master=info_frame, text="Settings", font=default_font_name + ' 11')
github_button.bind(
    "<Button-1>", lambda e: open_url("https://github.com/cycool29/coffeetime"))
sponsor_button.bind(
    "<Button-1>", lambda e: open_url("https://buymeacoffee.com/cycool29"))
quit_button.bind("<Button-1>", lambda e: window.destroy())
info_frame.pack(side="bottom",)
github_button.pack(side="left", padx=5, pady=5)
quit_button.pack(side="right", padx=5, pady=5)
settings_button.pack(side="right", padx=5, pady=5)
sponsor_button.pack(side="right", padx=5, pady=5)
tix.Balloon(window).bind_widget(github_button,
                                balloonmsg="View CoffeeTime GitHub page.")
tix.Balloon(window).bind_widget(sponsor_button,
                                balloonmsg="Buy cycool29 a coffee.")
tix.Balloon(window).bind_widget(quit_button, balloonmsg="Quit CoffeeTime.")
tix.Balloon(window).bind_widget(settings_button, balloonmsg="Change CoffeeTime settings.")

print(time_spinbox.get())

update_current_time_seconds()

window.mainloop()
