""""Implementation of a whist ui"""
from tkinter import Frame, Tk, Button, Text, LEFT, TOP, INSERT, Label, Entry
from math import floor
import random
import sys
from threading import Thread, Lock
import logger

NOBODY = "NONE"
MAX_ENTRIES = 10
LEFT_SHIFT = 160
FIELD_SPACE = 40
TITLE_SPACE = 200


log_history = "GAME LOGS: "
field_number = "-1"
window_open = False

ANTI_FLASH_WHITE = "#F0F2EF"
UMBER = "#5C5346"
SPICY_MIX = "#8C6057"
LIGHT_MOSS_GREEN = "#AFD5AA"

def to_int(curr_str):
    """Converts str to int, returns -1 if impossible"""
    try:
        return int(curr_str)
    except ValueError:
        return -1

def delete_children(window):
    """Delets everything on the window"""
    _list = window.winfo_children()

    for item in _list:
        item.destroy()


get_instance_guard = Lock()
destroy_instance_guard = Lock()

class WindowSingleton:
    '''Singleton for window'''
    __instance = None
    @staticmethod
    def get_instance():
        """ Static access method. """
        get_instance_guard.acquire()
        if WindowSingleton.__instance is None:
            WindowSingleton()
        get_instance_guard.release()
        return WindowSingleton.__instance
    @staticmethod
    def reset_instance():
        """Static use and destroy method"""
        window = WindowSingleton.__instance.window
        delete_children(window)
    @staticmethod
    def destroy_instance():
        """Destroys the current window"""
        destroy_instance_guard.acquire()
        if WindowSingleton.__instance is not None:
            WindowSingleton.__instance.window.destroy()
            WindowSingleton.__instance = None
        destroy_instance_guard.release()

    def __init__(self):
        """ Virtually private constructor. """
        if WindowSingleton.__instance is not None:
            pass
        else:
            self.window = Tk()
            WindowSingleton.__instance = self



def window_thread_start():
    """Creates the window(in a separate thread)"""
    window = WindowSingleton.get_instance().window
    global window_open
    width_value = window.winfo_screenwidth()
    height_value = window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (width_value, height_value))
    window_open = True
    window.mainloop()
    window_open = False
    sys.exit()

def start_window_thread():
    '''Starts the window thread'''
    window_thread = Thread(target=window_thread_start)
    window_thread.start()
    while window_open is False:
        pass


def get_players_number():
    '''gets players number'''

    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER

    curr_window = WindowSingleton.get_instance().window

    if window_open is False:
        raise IOError

    curr_window.title("Players number")
    curr_window.configure(background=background_color)

    title_text_label = Label(curr_window, text="Welcome to Whist", width=20, font=("bold", 30))
    #title_text_label.configure(anchor="n")
    title_text_label.place(x=400, y=30, anchor="w")
    title_text_label.configure(background=background_color, foreground=foreground_color)

    form_text_label = Label(curr_window, text="Insert number of players:",
                            width=20, font=("bold", 10), anchor="w")
    form_text_label.place(x=10, y=TITLE_SPACE)
    form_text_label.configure(background=background_color, foreground=foreground_color)

    number_entry = Entry(curr_window)
    number_entry.place(x=20, width=20, y=TITLE_SPACE+FIELD_SPACE)

    def get_val():
        """gets number from field"""
        global field_number

        field_number = number_entry.get()
        if int(field_number) < 4:
            form_text_label['text'] = "Too few players"
        elif int(field_number) > 6:
            form_text_label['text'] = "Too many players"

    done_button = Button(curr_window, fg=ANTI_FLASH_WHITE, bg=SPICY_MIX,
                         height=0, width=20, text="Done", command=get_val)
    done_button.place(x=20, y=TITLE_SPACE+FIELD_SPACE * 2)

    while not (4 <= to_int(field_number) <= 6) and window_open:
        pass
    WindowSingleton.reset_instance()
    return int(field_number)

def get_names_form(input_players_number):
    '''creates and shows name form'''
    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER

    try:
        input_players_number = int(input_players_number)
    except ValueError:
        raise ValueError

    if input_players_number < 2:
        raise ValueError

    curr_window = WindowSingleton.get_instance().window

    if window_open is False:
        raise IOError

    curr_window.title("Name form")
    curr_window.configure(background=background_color)
    text_label = Label(curr_window, text="Insert players names",
                       width=40, font=("bold", 20), anchor="w")
    text_label.place(x=380, y=53)
    text_label.configure(background=background_color, foreground=foreground_color)

    entries = []
    labels = []
    player_names = []
    for i in range(0, input_players_number):
        labels.append(Label(curr_window, background=background_color,
                            foreground=foreground_color, text="Player " + str(i + 1) +\
                            " name:", width=20, font=("bold", 10)))

        labels[i].place(x=LEFT_SHIFT*4*floor(i/MAX_ENTRIES),\
                          y=180+30*(i%MAX_ENTRIES))

        entries.append(Entry(curr_window))

        entries[i].place(x=LEFT_SHIFT*(4*(floor(i/MAX_ENTRIES))+1),\
                           y=180+30*(i % MAX_ENTRIES))


    logger.log_debug("Created name fields")

    def are_identical_names():
        identical_names = False
        players_number = len(player_names)
        for i in range(0, players_number):
            for j in range(0, players_number):
                if i != j:
                    if str(player_names[i]) == str(player_names[j]):
                        identical_names = True
        return identical_names

    def are_empty_names():
        empty_names = False
        players_number = len(player_names)
        if players_number == 0:
            return True
        for i in range(0, players_number):
            if player_names[i] == "":
                empty_names = True
        return empty_names

    def get_vals():
        '''gets emails from fields'''
        nonlocal player_names
        player_names = []
        for i in range(0, input_players_number):
            player_names.append(entries[i].get())
        identical_names = are_identical_names()
        empty_names = are_empty_names()
        if not (identical_names or empty_names):
            pass
        elif empty_names is True:
            text_label['text'] = "One or more names are empty"
        elif identical_names is True:
            text_label['text'] = "Two or more names are identical"

    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=get_vals)
    done_button.configure(background=SPICY_MIX, foreground=ANTI_FLASH_WHITE)
    done_button.place(x=20, y=130+35*(MAX_ENTRIES+1))
    while (are_empty_names() or are_identical_names()) and window_open:
        pass
    WindowSingleton.reset_instance()
    return player_names


def get_player_number_input(player_name, allowed_choices, input_type):
    """Functin used when the player has to insert a bid or result"""
    global field_number
    field_number = -1
    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER

    #return allowed_choices[random.randint(0, len(allowed_choices) - 1)]

    curr_window = WindowSingleton.get_instance().window
    curr_window.title("Players number")
    curr_window.configure(background=background_color)

    title_text_label = Label(curr_window, text="Whist " + input_type, width=20, font=("bold", 30))
    # title_text_label.configure(anchor="n")
    title_text_label.place(x=400, y=30, anchor="w")
    title_text_label.configure(background=background_color, foreground=foreground_color)

    form_text_label = Label(curr_window, text=player_name + ", insert your " +
                            input_type + "." + "Possible choices: " + str(allowed_choices),
                            width=40, font=("bold", 10), anchor="w")
    form_text_label.place(x=10, y=TITLE_SPACE)
    form_text_label.configure(background=background_color, foreground=foreground_color)

    #number_frame = Frame(curr_window)
    #number_frame.place(x=20, width=30, y=TITLE_SPACE + FIELD_SPACE)

    def element_in_list(numbers_list, queried_number):
        for number in numbers_list:
            if queried_number == number:
                return True
        return False

    def button_clicked(player_choice):
        """function called when player clicks a button"""
        def get_val():
            """gets number from field"""
            global field_number
            field_number = player_choice
        return get_val

    for i in range(0, len(allowed_choices)):
            option_button = Button(curr_window, fg="RED", height=1, width=5,
                                 text=str(allowed_choices[i]), command=button_clicked(allowed_choices[i]))
            option_button.place(x=25*(2*i+1), y=TITLE_SPACE + FIELD_SPACE, anchor="w")
            option_button.configure(background=SPICY_MIX, foreground=ANTI_FLASH_WHITE)

    while not element_in_list(allowed_choices, to_int(field_number)) and window_open:
        pass
    WindowSingleton.reset_instance()
    return int(field_number)


def show_info(curr_info):
    '''shows info, mostly for cop'''
    curr_window = WindowSingleton.get_instance().window
    curr_window.title("Night Report For Cop")
    screen_info = Text(curr_window)
    screen_info.insert(INSERT, curr_info)
    screen_info.pack()
    done_was_clicked = False
    def done_click():
        nonlocal done_was_clicked
        done_was_clicked = True
        WindowSingleton.reset_instance()
    done_button = Button(curr_window, fg="WHITE", background="RED", height=2, width=20,
                         text="Done", command=done_click)
    done_button.pack()
    while (not done_was_clicked) and window_open:
        pass
    logger.log_debug("Info window closed")


def show_scoreboard(player_names, target_round, scoreboard):
    """Shows scoreboard in window"""
    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER
    player_window = WindowSingleton.get_instance().window
    title_text_label = Label(player_window, text="SCOREBOARD\n\n", foreground=foreground_color,
                             background=background_color, width=20, font=("bold", 30))
    title_text_label.pack(side=TOP)
    player_frame = Frame(player_window, height=1, width=200)
    player_frame.pack(side=TOP)

    name_label = Label(player_frame, text="Players:", heigh=1, width=20,
                       background="black", foreground="white")
    name_label.pack(side=LEFT)
    for player_name in player_names:
        name_label = Label(player_frame, text=player_name, heigh=1, width=20,
                           background="black", foreground="white")
        name_label.pack(side=LEFT)

    for round_number in range(0, target_round + 1):

        round_frame = Frame(player_window, height=1, width=200)
        round_frame.pack(side=TOP)

        round_label = Label(round_frame, text="Round " + str(round_number + 1) + ":",
                            heigh=1, width=20, background="white", foreground="black")
        round_label.pack(side=LEFT)
        for player_score in scoreboard[round_number]:
            player_label = Label(round_frame, text=str(player_score), heigh=1, width=20,
                                 background="white", foreground="black")
            player_label.pack(side=LEFT)

    done_was_clicked = False

    def done_click():
        nonlocal done_was_clicked
        done_was_clicked = True
        WindowSingleton.reset_instance()

    done_button = Button(player_window, fg=ANTI_FLASH_WHITE, bg=SPICY_MIX,
                         height=2, width=20, text="Done", command=done_click)
    done_button.pack()
    while (not done_was_clicked) and window_open:
        pass

    WindowSingleton.reset_instance()
