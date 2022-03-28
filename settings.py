import tkinter as tk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import ImageTk, Image
import os


font = Gtk.Settings.get_default().get_property("gtk-font-name")
default_font_name = font.split(',')[0].replace(' ', '')
default_font_size = font[-2:]
default_font = default_font_name + ' ' + default_font_size
if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")
    
# default coffee break interval
# default notification message
# default notification sound


settings_window = tk.Tk()
icon_photo = tk.PhotoImage(file=f'{DIRECTORY}/icon.png')
settings_window.geometry("450x750+500+100")
settings_window.title('CoffeeTime Settings')
settings_window.iconphoto(False, icon_photo)


settings_title_frame = tk.Frame(master=settings_window)
logo_image = ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/proglogo.png"))
tk.Label(master=settings_title_frame, image=logo_image).pack()
settings_title_label = tk.Label(master=settings_title_frame, text='Settings\n', font=default_font_name + ' 25')
settings_title_label.pack()
settings_title_frame.pack()

default_coffee_break_frame = tk.Frame(master=settings_window)
default_coffee_break_label = tk.Label(master=default_coffee_break_frame, text='Default coffee break interval:', font=default_font)
default_coffee_break_spinbox = tk.Spinbox(master=default_coffee_break_frame, from_=1, to=10000,)
default_coffee_break_label.pack()
default_coffee_break_spinbox.pack()
default_coffee_break_frame.pack()

settings_window.mainloop()