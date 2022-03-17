import webbrowser
import os
os.environ['PYSTRAY_BACKEND'] = 'gtk'
from pystray import MenuItem as item
import pystray
import datetime
import tkinter as tk
from tkinter import tix
from PIL import ImageTk, Image
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")


def set_time():
    currentTime = datetime.datetime.now().strftime("%H:%M")
    time_label['text'] = "It's " + currentTime + ' now.\n'
    time_frame.after(1, set_time)

def quit_window(icon, item):
    icon.stop()
    window.destroy()

def show_window(icon, item):
    icon.stop()
    icon.visible = False
    window.after(0,window.deiconify)

def withdraw_window():  
    window.withdraw()
    menu = ( item('Show', show_window, default=True), item('Quit', quit_window))
    icon = pystray.Icon("name", icon_image, "title", menu)
    icon.visible = True
    icon.run()

def open_url(url):
    webbrowser.open(url)

font = Gtk.Settings.get_default().get_property("gtk-font-name")
default_font_name = font.split(',')[0].replace(' ', '')
default_font_size = font[-2:]
default_font = default_font_name + ' ' + default_font_size
icon_image = Image.open(f'{DIRECTORY}/icon.png')

# Create window
window = tix.Tk()
window.geometry("450x700+500+100")
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

spinbox_value = 0
spinbox_frame = tk.Frame(master=window,)
spinbox_separator = tk.Label(master=spinbox_frame, text='\n\nCoffee break interval:')
time_spinbox = tk.Spinbox(master=spinbox_frame, from_=0, to=30, wrap=True, textvariable=spinbox_value, )
spinbox_separator.pack()
time_spinbox.pack()
spinbox_frame.pack()

info_frame = tk.Frame(master=window,)
github_button = tk.Button(master=info_frame, text="GitHub", font=default_font)
sponsor_button = tk.Button(master=info_frame, text="Support", font=default_font)
github_button.bind("<Button-1>", lambda e: open_url("https://github.com/cycool29/coffeetime"))
sponsor_button.bind("<Button-1>", lambda e: open_url("https://buymeacoffee.com/cycool29"))
info_frame.pack(side="bottom",)
github_button.pack(side="left", padx=5, pady=5)
sponsor_button.pack(side="right", padx=5, pady=5)
tix.Balloon(window).bind_widget(github_button, balloonmsg="View CoffeeTime GitHub page.")
tix.Balloon(window).bind_widget(sponsor_button, balloonmsg="Buy cycool29 a coffee.")



set_time()
            

window.mainloop()
