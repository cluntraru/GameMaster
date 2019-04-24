'''Ui of mafia storyteller'''
from tkinter import Frame, Tk, Button, Text, Scrollbar, LEFT, \
    TOP, RIGHT, END, INSERT, Label, Entry, Listbox
from math import floor
import sys
from threading import Thread, Lock
import logger

NOBODY = "NONE"
MAX_ENTRIES = 10
LEFT_SHIFT = 160
FIELD_SPACE = 40
TITLE_SPACE = 200


assassinated_person = NOBODY
checked_person = NOBODY
saved_person = NOBODY
mutilated_person = NOBODY
mutilation_place = NOBODY
chosen_game = NOBODY
title_label_refrence = NOBODY
log_history = ["GAME LOGS: "]
field_number = "-1"

just_voted = False
window_open = False


ANTI_FLASH_WHITE = "#F0F2EF"
UMBER = "#5C5346"
SPICY_MIX = "#8C6057"
LIGHT_MOSS_GREEN = "#AFD5AA"
BROWN = "#281706"
LOG_SIZE = 40


def to_int(curr_str):
    """convers str to int, returns -1 if impossible"""
    try:
        return int(curr_str)
    except ValueError:
        return -1


def add_to_log_history(new_logs):
    """adds to log window"""
    global log_history
    if len(new_logs) <= 1:
        log_history.append("\n")
        return
    if new_logs[0] == '-':
        log_history.append(new_logs)
    else:
        for i in range(0, 1000):
            left_index = i * LOG_SIZE
            right_index = min(len(new_logs), (i + 1) * LOG_SIZE)
            log_history.append(new_logs[left_index:right_index])
            if right_index == len(new_logs):
                break
    log_history.append("\n")

def reset_log_history():
    """empties log window"""
    global log_history
    log_history = []
    log_history.append("GAME LOGS: ")


def delete_children(window):
    """Deletes everything on window"""
    _list = window.winfo_children()

    for item in _list:
        item.destroy()


GET_INSTANCE_GUARD = Lock()
DESTROY_INSTANCE_GUARD = Lock()

class WindowSingleton:
    '''Singleton for window'''
    __instance = None
    @staticmethod
    def get_instance():
        """ Mwthod for getting singleton instance """
        GET_INSTANCE_GUARD.acquire()
        if WindowSingleton.__instance is None:
            WindowSingleton()
        GET_INSTANCE_GUARD.release()
        return WindowSingleton.__instance
    @staticmethod
    def reset_instance():
        """Static method for resetting window method"""
        window = WindowSingleton.__instance.window
        delete_children(window)
    @staticmethod
    def destroy_instance():
        """Static method for destroying the window"""
        DESTROY_INSTANCE_GUARD.acquire()
        if WindowSingleton.__instance is not None:
            WindowSingleton.__instance.window.destroy()
            WindowSingleton.__instance = None
        DESTROY_INSTANCE_GUARD.release()

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


def close_window():
    """Closes the window if it is open"""
    global window_open
    while window_open is False:
        pass
    if window_open is True:
        WindowSingleton.destroy_instance()
        window_open = False
    return window_open


def get_players_number():
    '''gets players number'''

    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER

    add_to_log_history("")
    curr_window = WindowSingleton.get_instance().window

    if window_open is False:
        raise IOError

    #curr_window.geometry('500x500')
    curr_window.title("Players number")
    curr_window.configure(background=background_color)

    title_text_label = Label(curr_window, text="Welcome to Mafia", width=20, font=("bold", 30))
    #title_text_label.configure(anchor="n")
    title_text_label.place(x=480, y=30, anchor="w")
    title_text_label.configure(background=background_color, foreground=foreground_color)

    form_text_label = Label(curr_window, text="Insert number of players, between 4 and 21:",
                            width=35, font=("bold", 10), anchor="w")
    form_text_label.place(x=50, y=TITLE_SPACE)
    form_text_label.configure(background=background_color, foreground=foreground_color)

    number_entry = Entry(curr_window)
    number_entry.place(x=55, width=30, y=TITLE_SPACE+FIELD_SPACE)

    def get_val():
        """gets number from field"""
        global field_number

        field_number = number_entry.get()
        if not 4 < to_int(field_number) <= 20:
            form_text_label['text'] = "Ilegal number of players"

    done_button = Button(curr_window, fg="RED", height=0, width=20, text="Done", command=get_val)
    done_button.place(x=55, y=TITLE_SPACE+FIELD_SPACE * 2)
    done_button.configure(background=SPICY_MIX, foreground=ANTI_FLASH_WHITE)

    while (not 4 < to_int(field_number) <= 20) and window_open:
        pass
    WindowSingleton.reset_instance()
    return int(field_number)


def get_emails_form(arg_players_number):
    '''creates and shows email form'''

    try:
        arg_players_number = int(arg_players_number)
    except ValueError:
        raise ValueError

    if arg_players_number < 2:
        raise ValueError
    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER
    curr_window = WindowSingleton.get_instance().window

    if window_open is False:
        raise IOError

    curr_window.title("Email form")
    curr_window.configure(background=background_color)
    text_label = Label(curr_window, text="Insert players emails and names",
                       width=40, font=("bold", 20), anchor="w")
    text_label.place(x=480, y=53)
    text_label.configure(background=background_color, foreground=foreground_color)

    entries = []
    labels = []
    emails_and_names = []
    for i in range(0, arg_players_number):
        labels.append(Label(curr_window, background=background_color,
                            foreground=foreground_color, text="Player " + str(i + 1) +\
                            " name:", width=20, font=("bold", 10)))

        labels[i*2].place(x=LEFT_SHIFT*4*floor(i/MAX_ENTRIES),\
                          y=180+30*(i%MAX_ENTRIES))

        entries.append(Entry(curr_window))

        entries[i*2].place(x=LEFT_SHIFT*(4*(floor(i/MAX_ENTRIES))+1),\
                           y=180+30*(i % MAX_ENTRIES))

        labels.append(Label(curr_window, background=background_color, foreground=foreground_color,
                            text="Player " + str(i + 1) +\
                            " email:", width=20, font=("bold", 10)))

        labels[i * 2 + 1].place(x=LEFT_SHIFT * (4 * floor(i / MAX_ENTRIES) + 2),\
                                y=180 + 30 * (i % MAX_ENTRIES))

        entries.append(Entry(curr_window))

        entries[i * 2 +1].place(x=LEFT_SHIFT * (4 * floor(i / MAX_ENTRIES) + 3),\
                                y=180 + 30 * (i % MAX_ENTRIES))

    logger.log_debug("Created email fields")

    def are_identical_names():
        '''checks if there are identical names in the form'''
        identical_names = False
        nonlocal emails_and_names
        players_number = len(emails_and_names)
        try:
            for i in range(0, players_number):
                for j in range(0, players_number):
                    if i != j:
                        if emails_and_names[i][0] == emails_and_names[j][0]:
                            identical_names = True
        except IndexError:
            identical_names = True
        return identical_names

    def are_empty_names():
        '''checks if there are empty names in the form'''
        empty_names = False
        nonlocal emails_and_names
        players_number = len(emails_and_names)
        if players_number != arg_players_number:
            empty_names = True
        try:
            for i in range(0, players_number):
                if emails_and_names[i][0] == "":
                    empty_names = True
        except IndexError:
            empty_names = True
        return empty_names

    def get_vals():
        '''gets emails from fields'''
        nonlocal emails_and_names
        emails_and_names = []
        for i in range(0, arg_players_number):
            if entries[i*2].get() != "":
                emails_and_names.append((entries[i*2].get(), entries[i * 2 + 1].get()))
        identical_names = are_identical_names()
        empty_names = are_empty_names()

        if not (identical_names or empty_names):
            pass
        else:
            text_label['text'] = "Empty or identical names"

    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=get_vals)
    done_button.configure(background=SPICY_MIX, foreground=ANTI_FLASH_WHITE)
    done_button.place(x=20, y=130+35*(MAX_ENTRIES+1))

    while (len(emails_and_names) != arg_players_number or are_empty_names()
           or are_identical_names()) and window_open:
        pass
        #logger.log_debug("Window for emails and names was closed\n")
    WindowSingleton.reset_instance()
    return emails_and_names


def show_answer(curr_info):
    '''shows query answer for cop'''
    curr_window = WindowSingleton.get_instance().window
    curr_window.title("Night Report For Cop")
    screen_info = Text(curr_window, bg="white", fg=UMBER)
    screen_info.insert(INSERT, curr_info)
    screen_info.pack()
    done_was_clicked = False
    def done_click():
        '''resets window after done is clicked'''
        nonlocal done_was_clicked
        done_was_clicked = True
        WindowSingleton.reset_instance()
    done_button = Button(curr_window, fg=ANTI_FLASH_WHITE, bg=SPICY_MIX,
                         height=2, width=20, text="Done", command=done_click)
    done_button.pack()
    while (not done_was_clicked) and window_open:
        pass
    logger.log_debug("Info window closed")

def create_voting_screen(player_names, vote_function,
                         player_message="Time to vote", reset_at_beggining=True, reset_at_end=True):
    '''voting screen populating function'''
    global window_open, just_voted, title_label_refrence, log_history
    while window_open is False:
        pass

    player_window = WindowSingleton.get_instance().window
    if reset_at_beggining is False:
        just_voted = False
        player_window.title(player_message)
        title_label_refrence.configure(text=player_message)
        while (not just_voted) and window_open:
            pass
        if reset_at_end is True:
            WindowSingleton.reset_instance()
        return
    WindowSingleton.reset_instance()
    background_color = ANTI_FLASH_WHITE
    player_window.configure(background=background_color)
    player_window.title(player_message)
    logs_frame = Frame(player_window)
    if player_message != "Chose a game to play!":
        logs_frame.pack(side=LEFT)

    scrollbar = Scrollbar(player_window)
    scrollbar.pack(side=RIGHT)
    logs_label = Listbox(logs_frame, height=60, width=30,
                         font=("bold", 10), background=BROWN,
                         foreground=ANTI_FLASH_WHITE, yscrollcommand=scrollbar.set)
    for individual_log in log_history:
        logs_label.insert(END, individual_log)
    logs_label.pack(side=TOP)

    game_frame = Frame(player_window)
    game_frame.configure(background=background_color)
    game_frame.pack(side=LEFT)

    title_frame = Frame(game_frame)
    title_frame.configure(background=background_color)
    title_frame.pack()
    text_label = Label(title_frame, text=player_message, width=40,
                       font=("bold", 20), bg=UMBER, fg=ANTI_FLASH_WHITE,
                       anchor="w", justify="center")
    title_label_refrence = text_label
    text_label.pack()

    top_frame = Frame(game_frame)
    top_frame.pack()
    top_frame.configure(background=background_color)

    bottom_frame = Frame(game_frame)
    bottom_frame.pack()
    bottom_frame.configure(background=background_color)

    number_of_players = len(player_names)
    for i in range(0, number_of_players):
        player_name = player_names[i]
        if i < number_of_players / 2:
            curr_frame = top_frame
        else:
            curr_frame = bottom_frame
        vote_button = Button(curr_frame, bg=SPICY_MIX, font=("Courier", 10),
                             fg=ANTI_FLASH_WHITE, height=20, width=17,
                             text=player_name, command=vote_function(player_name))
        vote_button.pack(side=LEFT)

    just_voted = False
    while (not just_voted) and window_open:
        pass

    if reset_at_end is True:
        WindowSingleton.reset_instance()
    #logger.log_debug("Voting screen closed")


def day_vote(players_can_vote, votable_players):
    '''creates screen for day vote'''
    player_votes = {}
    for player_name in votable_players:
        player_votes[player_name] = 0
    player_votes[NOBODY] = 0
    for i in range(0, len(players_can_vote)):
        reset_at_beggining = bool(i == 0)
        reset_at_end = bool(i == (len(players_can_vote) - 1))
        player_name = players_can_vote[i]
        curr_player = player_name
        player_message = "DAY PHASE: " + curr_player + " votes "

        def day_vote_function(player_name):
            def callback():
                player_votes[player_name] += 1
                global just_voted
                just_voted = True
            return callback

        create_voting_screen(votable_players, day_vote_function,
                             player_message=player_message,
                             reset_at_beggining=reset_at_beggining, reset_at_end=reset_at_end)

    hanged_player = NOBODY
    for player_name in votable_players:
        if player_votes[player_name] > len(players_can_vote) / 2:
            hanged_player = player_name
    logger.log_debug("The day victim was: " + hanged_player)
    return hanged_player


def night_assassin_vote(town_names):
    '''creates window for assassin vote'''
    global assassinated_person
    assassinated_person = NOBODY
    player_message = "NIGHT PHASE: Assassins kill: "

    def assassin_vote_function(player_name):
        '''returns the function that gets the assassinated person'''
        def callback():
            '''function that gets the assassinated person'''
            global assassinated_person
            assassinated_person = player_name
            global just_voted
            just_voted = True

        return callback

    create_voting_screen(town_names, assassin_vote_function,
                         player_message=player_message)

    logger.log_debug("Night victim was " + assassinated_person)
    return assassinated_person


def night_cop_vote(player_names):
    '''creates window for cop vote'''
    global checked_person
    checked_person = NOBODY
    player_message = "NIGHT PHASE: Cop checks: "

    def cop_vote_function(player_name):
        '''returns function that gets the assassinated person'''
        def callback():
            '''function that gets the checked person'''
            global checked_person
            checked_person = player_name
            global just_voted
            just_voted = True

        return callback

    create_voting_screen(player_names, cop_vote_function,
                         player_message=player_message)

    logger.log_debug("Cop checked " + checked_person)
    return checked_person


def night_doctor_vote(player_names):
    '''creates window for doctor vote'''
    global saved_person
    saved_person = NOBODY
    player_message = "NIGHT PHASE: Doctor saves: "

    def doctor_vote_function(player_name):
        '''returns the function that gets the saved person'''
        def callback():
            '''function that gets the saved person'''
            global saved_person
            saved_person = player_name
            global just_voted
            just_voted = True

        return callback

    create_voting_screen(player_names, doctor_vote_function,
                         player_message=player_message)

    logger.log_debug("Doctor saved " + saved_person)
    return saved_person


def night_mutilator_vote(player_names):
    '''creates 2 screens for mutilator vote: one for choosing the player,
    the other for choosing the mutilation place'''
    global mutilated_person, mutilation_place
    mutilated_person = NOBODY
    mutilation_place = NOBODY
    def mutilator_vote_function(player_name):
        '''returns function that gets the mutilated person'''
        def callback():
            '''function that gets the mutilated person'''
            global mutilated_person
            mutilated_person = player_name
            global just_voted
            just_voted = True

        return callback

    def mutilator_place_function(place_name):
        '''returns function that gets the mutilation place'''
        def callback():
            '''function that gets the mutilation place'''
            global mutilation_place
            mutilation_place = place_name[0]
            global just_voted
            just_voted = True

        return callback

    player_message = "NIGHT PHASE: Mutilator mutilates: "
    create_voting_screen(player_names, mutilator_vote_function,
                         player_message=player_message)

    if mutilated_person != NOBODY:
        curr_window = WindowSingleton.get_instance().window
        curr_window.title("NIGHT PHASE: " + "Mutilator mutilates: ")
        create_voting_screen(["Hand", "Mouth"], mutilator_place_function,
                             player_message=player_message)

    logger.log_debug("Mutilator targeted " + mutilated_person)
    return (mutilated_person, mutilation_place)

def show_game_logs(player_data):
    '''Creates window with logs at the end of the game'''
    background_color = ANTI_FLASH_WHITE
    foreground_color = UMBER

    curr_window = WindowSingleton.get_instance().window

    if window_open is False:
        raise IOError

    # curr_window.geometry('500x500')
    curr_window.title("Game results")
    curr_window.configure(background=background_color)

    title_text_label = Label(curr_window, text="Game results", width=20, font=("bold", 30))
    # title_text_label.configure(anchor="n")
    screen_width = curr_window.winfo_screenwidth()
    screen_height = curr_window.winfo_screenheight()
    title_text_label.place(x=screen_width / 3, y=30, anchor="w")
    title_text_label.configure(background=background_color, foreground=foreground_color,
                               justify="left")

    lines_nr = 2 * len(player_data.split('\n'))

    form_text_label = Label(curr_window, text=player_data,
                            width=100, height=lines_nr, font=("bold", 10), anchor="w")
    form_text_label.place(x=screen_width / 2.5, y=screen_height/8)
    form_text_label.configure(background=background_color, foreground=foreground_color,
                              justify="left")

    def destroy_window():
        """Closes the tkinter window"""
        WindowSingleton.destroy_instance()

    done_button = Button(curr_window, fg="RED", height=0, width=20, text="Done",
                         command=destroy_window)
    done_button.place(x=screen_width / 2.5, y=screen_height/2 + lines_nr * 3)
    done_button.configure(background=SPICY_MIX, foreground=ANTI_FLASH_WHITE)
#start_window_thread()
#show_game_logs("m\np\n\nt\np\np\np\n\ns\np\n")
