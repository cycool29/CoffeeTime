from tkinter import filedialog 
import tkinter as tk
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from PIL import ImageTk, Image
import os
import configparser
import plyer

font = Gtk.Settings.get_default().get_property("gtk-font-name")
default_font_name = font.split(',')[0].replace(' ', '')
default_font_size = font[-2:]
default_font = default_font_name + ' ' + default_font_size
if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")
config = configparser.ConfigParser()
config.read(DIRECTORY + '/configurations.ini')
coffee_break_interval = config['CoffeeTime']['coffee_break_interval']
coffee_break_message = config['CoffeeTime']['coffee_break_message']
coffee_break_sound = config['CoffeeTime']['coffee_break_sound']
coffee_or_water = config['CoffeeTime']['coffee_or_water']
ramdom_daily_quotes = config['CoffeeTime']['ramdom_daily_quotes']

# default coffee break interval
# default notification message
# default notification sound
# notiification sound?
# water or coffee
# random daily quote
# theme

class SettingsWindow:
    def launch_window(self):
        self.settings_window.geometry("450x750+500+100")
        self.settings_window.title('CoffeeTime Settings')
        self.settings_window.iconphoto(False, self.icon_photo)
        tk.Label(master=self.settings_title_frame, image=self.logo_image).pack()
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
        self.settings_window = tk.Tk()
        self.coffee_break_interval_stringvar = tk.StringVar(value=coffee_break_interval)
        self.coffee_break_message_stringvar = tk.StringVar(value=coffee_break_message)
        self.theme_stringvar = tk.StringVar(value='light')
        
        self.settings_title_frame = tk.Frame(master=self.settings_window)
        self.logo_image = ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/proglogo.png"))
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

settings_window = SettingsWindow()

if __name__ == '__main__':
    settings_window.launch_window()