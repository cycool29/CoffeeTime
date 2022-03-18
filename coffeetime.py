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
from itertools import count
import PySimpleGUI as sg


if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")


def update_current_time():
    currentTime = datetime.datetime.now().strftime("%H:%M")
    time_label['text'] = "It's " + currentTime + ' now.\n'
    time_frame.after(1, update_current_time)


def quit_window(icon, item):
    icon.stop()
    window.destroy()


def show_window(icon, item):
    icon.stop()
    icon.visible = False
    window.after(0, window.deiconify)


def withdraw_window():
    window.withdraw()
    menu = (item('Show', show_window, default=True), item('Quit', quit_window))
    icon = pystray.Icon("name", icon_image, "title", menu)
    icon.visible = True
    icon.run()


def open_url(url):
    webbrowser.open(url)


def print_spinbox_value():
    pass

def open_popup():
    top = tk.Toplevel(window)
    top.geometry("750x250")
    top.title("Child Window")
    tk.Label(top, text="Hello World!", font=(
        'Mistral 18 bold')).place(x=150, y=80)


class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


font = Gtk.Settings.get_default().get_property("gtk-font-name")
default_font_name = font.split(',')[0].replace(' ', '')
default_font_size = font[-2:]
default_font = default_font_name + ' ' + default_font_size
icon_image = Image.open(f'{DIRECTORY}/icon.png')


# Create window
window = tix.Tk()
window.geometry("450x750+500+100")
window.title('CoffeeTime')
window.iconphoto(False, tk.PhotoImage(file=f'{DIRECTORY}/icon.png'))
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
                          textvariable=spinbox_value, font=default_font, command=print_spinbox_value, width=10)
time_unit = tk.Label(master=spinbox_frame, text=' minutes', font=default_font)
spinbox_separator.pack()
time_spinbox.pack(side=tk.LEFT)
time_unit.pack(side=tk.RIGHT)
spinbox_frame.pack()


def coffee_break_countdown():
    countdown_time = int(time_spinbox.get())*60
    start_time = (int(startfrom_hour_value.get())*3600) + (int(startfrom_minutes_value.get())*60)
    current_time = int(datetime.datetime.now().strftime("%H"))*3600 + int(datetime.datetime.now().strftime("%M"))*60
    
    print('Countdown time: ' + str(countdown_time))
    print('Start time: ' + str(start_time))
    print('Current time: ' + str(current_time))
    
    next_break_time_system = start_time + countdown_time
    next_break_time_user = str(next_break_time_system / 3600).split('.')[0] + ':' + str((next_break_time_system % 3600) / 60).split('.')[0]

    while True:
        if next_break_time_system >= current_time:
            break
        else:
            next_break_time_system += countdown_time
            print(next_break_time_system)
        
    next_break_time_interval_system  = next_break_time_system - current_time
    next_break_time_interval_user = str(next_break_time_interval_system / 60).split('.')[0]   
    
    lefttime_label['text'] = "\nYour next coffee break is at " + next_break_time_interval_user + ' minutes later.'
    window.update()

    while True:
        try:
            if int(datetime.datetime.now().strftime("%H"))*3600 + int(datetime.datetime.now().strftime("%M"))*60 != next_break_time_system:
                countdown_time = int(time_spinbox.get())*60
                start_time = (int(startfrom_hour_value.get())*3600) + (int(startfrom_minutes_value.get())*60)
                current_time = int(datetime.datetime.now().strftime("%H"))*3600 + int(datetime.datetime.now().strftime("%M"))*60
                
                print('Countdown time: ' + str(countdown_time))
                print('Start time: ' + str(start_time))
                print('Current time: ' + str(current_time))
                
                next_break_time_system = start_time + countdown_time
                next_break_time_user = str(next_break_time_system / 3600).split('.')[0] + ':' + str((next_break_time_system % 3600) / 60).split('.')[0]

                while True:
                    if next_break_time_system >= current_time:
                        break
                    else:
                        next_break_time_system += countdown_time
                        print(next_break_time_system)
                    
                next_break_time_interval_system  = next_break_time_system - current_time
                next_break_time_interval_user = str(next_break_time_interval_system / 60).split('.')[0]   
                
                lefttime_label['text'] = "\nYour next coffee break is at " + next_break_time_interval_user + ' minutes later.'
                window.update()
                time.sleep(1)
            else:
                sg.Window('Coffee break', [
                            [sg.T("Hey, it's time to take a coffee break.\n")], [sg.Button(s=10, button_text='Dismiss'), sg.Button(s=10, button_text='Snooze')]]).read(close=True)
        except:
            pass

# Start from spinbox
startfrom_hour_value = tk.StringVar(window)
startfrom_hour_value.set(str(datetime.datetime.now().strftime("%H")))
startfrom_minutes_value = tk.StringVar(window)
startfrom_minutes_value.set(str(datetime.datetime.now().strftime("%M")))
startfrom_frame = tk.Frame(master=window)
start_from_label = tk.Label(master=startfrom_frame,
                            text='\nStart from:', font=default_font)
start_from_hour_spinbox = tk.Spinbox(master=startfrom_frame, from_=0, to=24,
                                     wrap=True, font=default_font, width=10, textvariable=startfrom_hour_value)
start_from_separator = tk.Label(
    master=startfrom_frame, text=':', font=default_font)
start_from_minutes_spinbox = tk.Spinbox(master=startfrom_frame, from_=0, to=60,
                                        wrap=True, font=default_font, width=10, textvariable=startfrom_minutes_value)
start_button = tk.Button(master=startfrom_frame, text='Start', command=coffee_break_countdown, font=default_font)
start_from_label.pack()
start_button.pack(side=tk.BOTTOM, pady=10)
start_from_hour_spinbox.pack(side=tk.LEFT, padx=10)
start_from_minutes_spinbox.pack(side=tk.RIGHT, padx=10)
start_from_separator.pack(side=tk.RIGHT)
startfrom_frame.pack()


# Left time
lefttime_frame = tk.Label(master=window)
lefttime_label = tk.Label(master=lefttime_frame, text='', font=default_font_name + ' 11')
lefttime_label.pack()
lefttime_frame.pack()

# Info frame
info_frame = tk.Frame(master=window)
github_button = tk.Button(master=info_frame, text="GitHub", font=default_font)
sponsor_button = tk.Button(
    master=info_frame, text="Support", font=default_font)
quit_button = tk.Button(master=info_frame, text="Quit", font=default_font)
github_button.bind(
    "<Button-1>", lambda e: open_url("https://github.com/cycool29/coffeetime"))
sponsor_button.bind(
    "<Button-1>", lambda e: open_url("https://buymeacoffee.com/cycool29"))
quit_button.bind("<Button-1>", lambda e: window.destroy())
info_frame.pack(side="bottom",)
github_button.pack(side="left", padx=5, pady=5)
quit_button.pack(side="right", padx=5, pady=5)
sponsor_button.pack(side="right", padx=5, pady=5)
tix.Balloon(window).bind_widget(github_button,
                                balloonmsg="View CoffeeTime GitHub page.")
tix.Balloon(window).bind_widget(sponsor_button,
                                balloonmsg="Buy cycool29 a coffee.")
tix.Balloon(window).bind_widget(quit_button, balloonmsg="Quit CoffeeTime.")

print(time_spinbox.get())

update_current_time()

window.mainloop()
