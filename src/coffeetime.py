from doctest import master
from PIL import ImageGrab
import configparser  # nopep8
import threading  # nopep8
import os  # nopep8
if os.name == 'nt':
    RUNNING_ON_WINDOWS = True
    import ctypes

if os.name == 'posix':
    RUNNING_ON_WINDOWS = False
    import gi  # nopep8
    gi.require_version('Gtk', '3.0')  # nopep8
    from gi.repository import Gtk  # nopep8

from PIL import ImageTk, Image  # nopep8
from tkinter import tix  # nopep8
import tkinter as tk  # nopep8
import datetime  # nopep8
import webbrowser  # nopep8
import PySimpleGUIQt as sg  # nopep8
import plyer
import playsound

if "DIRECTORY" not in os.environ:
    DIRECTORY = os.path.dirname(os.path.abspath(__file__))
else:
    DIRECTORY = os.getenv("DIRECTORY")

stop_timer_thread = False
show_notification = True

if os.name == 'posix':
    font = Gtk.Settings.get_default().get_property("gtk-font-name")
    default_font_name = font.split(',')[0].replace(' ', '')
    default_font_size = font[-2:]
    default_font = (default_font_name, default_font_size)
else:
    default_font_name = 'Segoe UI'
    default_font_size = '12'
    default_font = ('Segoe UI', 12)

config = configparser.ConfigParser()
config.read(DIRECTORY + '/configurations.ini')
coffee_break_interval = config['CoffeeTime']['coffee_break_interval']
coffee_break_message = config['CoffeeTime']['coffee_break_message']
coffee_break_sound = config['CoffeeTime']['coffee_break_sound']
coffee_or_water = config['CoffeeTime']['coffee_or_water']
ramdom_daily_quotes = config['CoffeeTime']['ramdom_daily_quotes']
theme = config['CoffeeTime']['theme']


def open_subwindow(window):
    x = window()
    cycool29_is_very_cool = x.window.after(0, x.launch_window())
    del cycool29_is_very_cool


timer_event = threading.Event()
timer_after_id = None


class CoffeeTimeTimer:
    def __init__(self):
        self.current_countdown_time_seconds = int(
            main_window.time_spinbox.get()) * 60
        self.total_countdown_time_seconds = self.current_countdown_time_seconds
        self.refresh_curent_time()

    def refresh_curent_time(self):
        self.current_time_seconds = int(datetime.datetime.now().strftime(
            "%H")) * 3600 + int(datetime.datetime.now().strftime(
                "%M")) * 60
        return self.current_time_seconds

    def refresh_break_time(self):
        self.next_break_time_seconds = self.current_time_seconds + \
            self.current_countdown_time_seconds
        self.next_break_time_interval_seconds = self.next_break_time_seconds - \
            self.current_time_seconds
        self.next_break_time_interval_user = self.next_break_time_interval_seconds / 60

    def refresh_lefttime_label(self):
        try:
            if self.next_break_time_interval_user == 1:  # 1 minute later
                main_window.lefttime_label['text'] = "\nYour next coffee break is at a minute later."
                main_window.lefttime_label.pack()
            elif self.next_break_time_interval_user > 1:  # More than 1 minute later
                main_window.lefttime_label['text'] = "\nYour next coffee break is at about " + str(
                    self.next_break_time_interval_user).split(
                    '.')[0] + " minutes later."
                main_window.lefttime_label.pack()
            elif self.next_break_time_interval_user < 1:  # Less than 1 minute later
                main_window.lefttime_label['text'] = "\nYour next coffee break is at less than a minute later."
                main_window.lefttime_label.pack()
            else:
                pass
        except:
            pass

    def refresh_current_countdown_time(self):
        self.current_countdown_time_seconds = total_countdown_time_requested
        self.total_countdown_time_seconds = self.current_countdown_time_seconds

    def timer(self):
        global timer_after_id
        timer_after_id = None
        if self.current_countdown_time_seconds > 0:
            # try:
            print(self.current_countdown_time_seconds)
            self.refresh_curent_time()
            self.refresh_break_time()
            self.refresh_lefttime_label()

            # maybe user changed the requested timer seconds
            if total_countdown_time_requested == self.total_countdown_time_seconds:
                self.current_countdown_time_seconds -= 1
            else:
                self.refresh_current_countdown_time()  # restart whole timer
        else:
            if total_countdown_time_requested != 0:
                open_subwindow(NotificationWindow)
                print('Coffee break is over!')
                self.refresh_current_countdown_time()

                print('Timer Done')

        timer_after_id = main_window.lefttime_label.after(1000, self.timer)

    def coffee_break_countdown(self):
        if timer_after_id is not None:
            main_window.lefttime_label.after_cancel(timer_after_id)
        self.refresh_break_time()
        self.refresh_lefttime_label()
        self.refresh_current_countdown_time()

        self.timer()

    def start_coffee_break_countdown(self, *args):
        global total_countdown_time_requested
        total_countdown_time_requested = int(
            main_window.time_spinbox.get()) * 60
        # if timer_thread.is_alive() == False:
        self.coffee_break_countdown()
        withdraw_window()


class MainWindow:
    def update_current_time_seconds(self):
        current_time = datetime.datetime.now().strftime("%H:%M")
        self.time_label['text'] = "It's " + current_time + ' now.\n'
        self.window.after(1, self.update_current_time_seconds)

    def launch_window(self):
        self.window.protocol('WM_DELETE_WINDOW',
                             lambda: withdraw_window(self.window))
        if theme.lower() == 'light':
            self.window.tk_setPalette(background='#d3d3d3')
        elif theme.lower() == 'dark':
            self.window.tk_setPalette(background='#1b1c1e')
        self.window.title("CoffeeTime")
        self.window.geometry("600x750+" + str(int(screen_width / 2 - 300)) +
                             "+" + str(int(screen_height / 2 - 450)))

        self.window.wm_iconphoto(
            True, ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/icon.png"), master=self.window))
        self.window.deiconify()
        self.time_spinbox.pack()
        self.start_button.pack()

        # Logo frame
        self.logo_image_top.pack()
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
            "<Button-1>",
            lambda e: open_url("https://github.com/cycool29/CoffeeTime"))
        self.sponsor_button.bind(
            "<Button-1>",
            lambda e: open_url("https://ko-fi.com/cycool29"))
        self.quit_button.bind("<Button-1>", self.quit_coffeetime)
        self.start_button.bind(
            "<Button-1>", timer.start_coffee_break_countdown)
        self.info_frame.pack(side="bottom", )
        self.github_button.pack(side="left", padx=5, pady=5)
        self.quit_button.pack(side="right", padx=5, pady=5)
        self.settings_button.pack(side="right", padx=5, pady=5)
        self.sponsor_button.pack(side="right", padx=5, pady=5)
        tix.Balloon(self.window).bind_widget(
            self.github_button, balloonmsg="View CoffeeTime GitHub page.")
        tix.Balloon(self.window).bind_widget(
            self.sponsor_button, balloonmsg="Buy cycool29 a coffee.")
        tix.Balloon(self.window).bind_widget(self.quit_button,
                                             balloonmsg="Quit CoffeeTime.")
        tix.Balloon(self.window).bind_widget(
            self.settings_button, balloonmsg="Change CoffeeTime settings.")

        self.update_current_time_seconds()

        self.window.after(0, lambda: self.window.focus_force())

        self.window.mainloop()

    def quit_coffeetime(self, *args):
        quit_coffeetime()

    def show_window(self):
        self.window.wm_deiconify()

    def __init__(self) -> None:
        self.window = tix.Tk()
        self.logo_frame = tk.Frame(master=self.window)
        if theme.lower() == 'light':
            self.logo_image = ImageTk.PhotoImage(
                Image.open(f"{DIRECTORY}/proglogo-in-light-theme.png"))
        elif theme.lower() == 'dark':
            self.logo_image = ImageTk.PhotoImage(
                Image.open(f"{DIRECTORY}/proglogo-in-dark-theme.png"))
        self.logo_image_top = tk.Label(
            master=self.logo_frame, image=self.logo_image)
        self.time_frame = tk.Frame(master=self.window)
        self.time_label = tk.Label(master=self.time_frame,
                                   text="",
                                   font=(default_font_name, 20))
        self.quote_label = tk.Label(
            master=self.time_frame,
            text="Focus, do what you do best.\nI will remind you when you need a rest. ;)",
            font=default_font)
        self.coffee_break_interval_stringvar = tk.StringVar(
            value=coffee_break_interval)
        self.spinbox_frame = tk.Frame(master=self.window, )
        self.spinbox_separator = tk.Label(master=self.window,
                                          text='\n\nCoffee break interval:',
                                          font=default_font)
        self.time_spinbox = tk.Spinbox(master=self.spinbox_frame,
                                       from_=0,
                                       to=10000,
                                       font=default_font,
                                       width=12,
                                       textvariable=self.coffee_break_interval_stringvar)
        self.time_unit = tk.Label(master=self.spinbox_frame,
                                  text=' minutes',
                                  font=default_font)
        self.start_frame = tk.Frame(master=self.window)
        self.start_button = tk.Button(master=self.start_frame,
                                      text='Start',
                                      font=default_font)
        self.lefttime_frame = tk.Label(master=self.window)
        self.lefttime_label = tk.Label(master=self.lefttime_frame,
                                       text='',
                                       font=(default_font_name, 11))
        self.info_frame = tk.Frame(master=self.window)
        self.github_button = tk.Button(master=self.info_frame,
                                       text="GitHub",
                                       font=(default_font_name, 11))
        self.sponsor_button = tk.Button(master=self.info_frame,
                                        text="Support",
                                        font=(default_font_name, 11))
        self.quit_button = tk.Button(master=self.info_frame,
                                     text="Quit",
                                     font=(default_font_name, 11))
        self.settings_button = tk.Button(
            master=self.info_frame,
            text="Settings",
            font=(default_font_name, 11),
            command=lambda: open_subwindow(SettingsWindow))


# default coffee break interval
# default notification message
# default notification sound
# notiification sound?
# water or coffee
# random daily quote
# theme


class SettingsWindow:

    def launch_window(self):
        if theme.lower() == 'light':
            self.window.tk_setPalette(background='#d3d3d3')
        elif theme.lower() == 'dark':
            self.window.tk_setPalette(background='#1b1c1e')
        self.window.geometry("600x750+" + str(int(screen_width / 2 - 300)) +
                             "+" + str(int(screen_height / 2 - 450)))

        self.window.wm_iconphoto(
            True, ImageTk.PhotoImage(Image.open(f"{DIRECTORY}/icon.png"), master=self.window))
        self.window.geometry("600x750+" + str(int(screen_width / 2 - 300)) +
                             "+" + str(int(screen_height / 2 - 450)))
        self.window.title('CoffeeTime Settings')
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
        self.separator_between_save_button_and_theme_spinbox.pack()
        self.save_settings_button.pack()
        self.window.after(
            1, lambda: self.window.focus_force())
        self.window.mainloop()

    def update_config(self):
        global theme
        global coffee_break_interval
        global coffee_break_message
        global coffee_break_sound
        global coffee_or_water
        global random_daily_quotes

        config['CoffeeTime'][
            'coffee_break_interval'] = self.coffee_break_interval_spinbox.get(
        )
        config['CoffeeTime'][
            'coffee_break_message'] = self.coffee_break_message_entry.get()
        config['CoffeeTime']['coffee_break_sound'] = self.coffee_break_sound
        config['CoffeeTime']['theme'] = self.theme_spinbox.get().lower()

        with open(DIRECTORY + '/configurations.ini', 'w') as configfile:
            config.write(configfile)

        config.read(DIRECTORY + '/configurations.ini')
        coffee_break_interval = config['CoffeeTime']['coffee_break_interval']
        coffee_break_message = config['CoffeeTime']['coffee_break_message']
        coffee_break_sound = config['CoffeeTime']['coffee_break_sound']
        coffee_or_water = config['CoffeeTime']['coffee_or_water']
        ramdom_daily_quotes = config['CoffeeTime']['ramdom_daily_quotes']
        theme = config['CoffeeTime']['theme']

        if theme.lower() == 'light':
            main_window.logo_image.__del__()
            main_window.logo_image = ImageTk.PhotoImage(
                Image.open(f"{DIRECTORY}/proglogo-in-light-theme.png"))
            main_window.logo_image_top.configure(image=main_window.logo_image)
            main_window.logo_image_top.pack()
            main_window.window.tk_setPalette(background='#d3d3d3')
            self.window.tk_setPalette(background='#d3d3d3')
        elif theme.lower() == 'dark':
            main_window.logo_image.__del__()
            main_window.logo_image = ImageTk.PhotoImage(
                Image.open(f"{DIRECTORY}/proglogo-in-dark-theme.png", ))
            main_window.logo_image_top.configure(image=main_window.logo_image)
            main_window.logo_image_top.pack()
            main_window.window.tk_setPalette(background='#1b1c1e')
            self.window.tk_setPalette(background='#1b1c1e')

        main_window.coffee_break_interval_stringvar.set(coffee_break_interval)

        main_window.window.update()
        self.window.update()

    def choose_sound_file(self):
        self.coffee_break_sound = \
            plyer.filechooser.open_file(filters=["*mp3", "*ogg", "*aac"], title='Choose a sound file',
                                        icon=f'{DIRECTORY}/icon.png')[0]
        if os.path.isfile(self.coffee_break_sound):
            self.update_config()

    def __init__(self) -> None:
        self.window = tk.Tk()
        print(coffee_break_interval)
        self.coffee_break_interval_stringvar = tk.StringVar(
            value=coffee_break_interval, master=self.window)
        self.coffee_break_message_stringvar = tk.StringVar(
            value=coffee_break_message, master=self.window)
        self.theme_stringvar = tk.StringVar(value=theme, master=self.window)
        if theme.lower() == 'dark':
            self.theme_values = ['Dark', 'Light']
        else:
            self.theme_values = ['Light', 'Dark']
        self.coffee_break_sound = ''

        self.settings_title_frame = tk.Frame(master=self.window)
        self.settings_title_label = tk.Label(master=self.settings_title_frame,
                                             text='Settings\n',
                                             font=(default_font_name, 25))

        self.coffee_break_interval_frame = tk.Frame(
            master=self.window)
        self.coffee_break_interval_label = tk.Label(
            master=self.coffee_break_interval_frame,
            text='Coffee break interval:',
            font=default_font)
        self.coffee_break_interval_spinbox = tk.Spinbox(
            master=self.coffee_break_interval_frame,
            from_=2,
            to=10000,
            textvariable=self.coffee_break_interval_stringvar,
            font=default_font,)

        self.coffee_break_message_frame = tk.Frame(master=self.window)
        self.coffee_break_message_label = tk.Label(
            master=self.coffee_break_message_frame,
            text='\nCoffee break message:',
            font=default_font)
        self.coffee_break_message_entry = tk.Entry(
            master=self.coffee_break_message_frame,
            textvariable=self.coffee_break_message_stringvar,
            font=default_font,)

        self.coffee_break_sound_frame = tk.Frame(master=self.window)
        self.coffee_break_sound_label = tk.Label(
            master=self.coffee_break_sound_frame,
            text='\nSelect a coffee break sound effect:',
            font=default_font)
        self.coffee_break_sound_button = tk.Button(
            master=self.coffee_break_sound_frame,
            text='Select file',
            font=default_font,
            command=self.choose_sound_file)

        self.theme_frame = tk.Frame(master=self.window)
        self.theme_label = tk.Label(master=self.theme_frame,
                                    text='\nSelect a theme:',
                                    font=default_font)
        self.theme_spinbox = tk.Spinbox(master=self.theme_frame,
                                        textvariable=self.theme_stringvar,
                                        font=default_font,
                                        values=self.theme_values,
                                        wrap=True)
        self.separator_between_save_button_and_theme_spinbox = tk.Label(
            master=self.theme_frame, text='\n')
        self.save_settings_button = tk.Button(
            master=self.window, text='Save', font=default_font, command=self.update_config)


class NotificationWindow:

    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.protocol('WM_DELETE_WINDOW', self.window.destroy())
        self.notification_image = ImageTk.PhotoImage(
            Image.open(f"{DIRECTORY}/icon.png").resize((100, 100), Image.ANTIALIAS), master=self.window)
        self.notification_image_label = tk.Label(
            master=self.window,  image=self.notification_image)
        self.notification_label = tk.Label(self.window,
                                           text="\nTake a coffee break!",
                                           font=default_font_name + " 20")
        self.logo_image = ImageTk.PhotoImage(
            Image.open(f"{DIRECTORY}/icon.png"), master=self.window)

    def launch_window(self):
        self.window.attributes('-topmost', 'true')
        self.window.iconphoto(False, self.logo_image)
        self.window.title("Coffee Break!")
        self.window.geometry("600x100+" +
                                          str(int(screen_width / 2 - 300)) +
                                          "+" +
                                          str(int(screen_height / 2 - 50)))
        self.window.resizable(False, False)
        self.notification_label.pack(side=tk.LEFT)
        self.notification_image_label.pack(side=tk.LEFT)
        self.window.mainloop()


def system_tray_icon():
    global tray
    menu_def = ['File', ['Show', 'Exit', 'Settings']]
    tray = sg.SystemTray(menu=menu_def,
                         filename=DIRECTORY + '/icon.png', tooltip='Launch CoffeeTime main window')

    while True:
        menu_item = tray.Read(timeout=0)
        if menu_item in ('Show', '__ACTIVATED__'):
            main_window.window.after(0, main_window.window.deiconify())
            main_window.window.after(
                0, main_window.window.attributes('-topmost', True))
            main_window.window.after(
                0, main_window.window.attributes('-topmost', False))
            main_window.window.after(0, main_window.window.focus_force())

        elif menu_item == 'Exit':
            quit_coffeetime()

        elif menu_item == 'Settings':
            open_subwindow(SettingsWindow)


main_window = MainWindow()


timer = CoffeeTimeTimer()


def withdraw_window(window=main_window.window):
    window.withdraw()


def open_url(url):
    webbrowser.open(url)


def quit_coffeetime():
    tray.Close()
    os._exit(0)


# if RUNNING_ON_WINDOWS:
#     user32 = ctypes.windll.user32
#     screen_width = user32.GetSystemMetrics(0)
#     screen_height = user32.GetSystemMetrics(1)
# else:
# screen_width = main_window.window.winfo_screenwidth()
# screen_height = main_window.window.winfo_screenheight()

screen_width, screen_height = ImageGrab.grab().size


img = ImageGrab.grab()


print(screen_height)
print(screen_width)

threading.Thread(target=system_tray_icon, name='CoffeeTime SysTray').start()

if __name__ == '__main__':
    main_window.launch_window()
