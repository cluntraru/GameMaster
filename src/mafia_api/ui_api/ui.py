'''Ui of mafia storyteller'''
from tkinter import Frame, Tk, Button, Text, Scrollbar, LEFT, TOP, RIGHT, END, INSERT, Label, Entry, Listbox
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
log_history = ["GAME LOGS: "]
field_number = "-1"
just_voted = False
window_open = False

ANTI_FLASH_WHITE = "#F0F2EF"
UMBER = "#5C5346"
SPICY_MIX = "#8C6057"
LIGHT_MOSS_GREEN = "#AFD5AA"


def to_int(curr_str):
    """convers str to int, returns -1 if impossible"""
    try:
        return int(curr_str)
    except ValueError:
        return -1


def add_to_log_history(new_logs):
    """adds to log window"""
    global log_history
    log_history.append(new_logs)
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
        """ Static access method. """
        GET_INSTANCE_GUARD.acquire()
        if WindowSingleton.__instance is None:
            WindowSingleton()
        GET_INSTANCE_GUARD.release()
        return WindowSingleton.__instance
    @staticmethod
    def reset_instance():
        """Static method for reseting window method"""
        window = WindowSingleton.__instance.window
        delete_children(window)
    @staticmethod
    def destroy_instance():
        """Static method for destroying window"""
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
    title_text_label.place(x=400, y=30, anchor="w")
    title_text_label.configure(background=background_color, foreground=foreground_color)

    form_text_label = Label(curr_window, text="Insert number of players, between 4 and 21:",
                            width=35, font=("bold", 10), anchor="w")
    form_text_label.place(x=10, y=TITLE_SPACE)
    form_text_label.configure(background=background_color, foreground=foreground_color)

    number_entry = Entry(curr_window)
    number_entry.place(x=20, width=20, y=TITLE_SPACE+FIELD_SPACE)

    def get_val():
        """gets number from field"""
        global field_number

        field_number = number_entry.get()
        if not 4 < to_int(field_number) <= 20:
            form_text_label['text'] = "Ilegal number of players"

    done_button = Button(curr_window, fg="RED", height=0, width=20, text="Done", command=get_val)
    done_button.place(x=20, y=TITLE_SPACE+FIELD_SPACE * 2)
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
    text_label.place(x=380, y=53)
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


def show_info(curr_info):
    '''shows info, mostly for cop'''
    curr_window = WindowSingleton.get_instance().window
    curr_window.title("Night Report For Cop")
    screen_info = Text(curr_window, bg="white", fg=UMBER)
    screen_info.insert(INSERT, curr_info)
    screen_info.pack()
    done_was_clicked = False
    def done_click():
        nonlocal done_was_clicked
        done_was_clicked = True
        WindowSingleton.reset_instance()
    done_button = Button(curr_window, fg=ANTI_FLASH_WHITE, bg=SPICY_MIX,
                         height=2, width=20, text="Done", command=done_click)
    done_button.pack()
    while (not done_was_clicked) and window_open:
        pass
    logger.log_debug("Info window closed")

def create_voting_screen(player_names, vote_function, player_message="Time to vote"):
    '''screen populating function'''
    global window_open
    while window_open is False:
        pass
    player_window = WindowSingleton.get_instance().window

    background_color = ANTI_FLASH_WHITE
    player_window.configure(background=background_color)
    player_window.title(player_message)
    logs_frame = Frame(player_window)
    if player_message != "Chose a game to play!":
        logs_frame.pack(side=LEFT)
    global log_history
    scrollbar = Scrollbar(player_window)
    scrollbar.pack(side=RIGHT)
    logs_label = Listbox(logs_frame, height=60, width=20,
                       font=("bold", 10), background=LIGHT_MOSS_GREEN,
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
        vote_button = Button(curr_frame, bg=SPICY_MIX,
                             fg=ANTI_FLASH_WHITE, height=20, width=17,
                             text=player_name, command=vote_function(player_name))
        vote_button.configure(font=("Courier", 10))
        vote_button.pack(side=LEFT)
    global just_voted
    just_voted = False
    while (not just_voted) and window_open:
        pass
    WindowSingleton.reset_instance()
    #logger.log_debug("Voting screen closed")


def day_vote(players_can_vote, votable_players):
    '''day vote'''
    player_votes = {}
    for player_name in votable_players:
        player_votes[player_name] = 0
    player_votes[NOBODY] = 0
    for player_name in players_can_vote:
        curr_player = player_name
        player_message = "DAY PHASE: " + curr_player + " votes "

        def day_vote_function(player_name):
            def callback():
                player_votes[player_name] += 1
                global just_voted
                just_voted = True
            return callback

        create_voting_screen(votable_players, day_vote_function,
                             player_message=player_message)

    hanged_player = NOBODY
    for player_name in votable_players:
        if player_votes[player_name] > len(players_can_vote) / 2:
            hanged_player = player_name
    logger.log_debug("The day victim was: " + hanged_player)
    return hanged_player


def game_choice(games_list):
    '''assassin vote'''
    global chosen_game
    chosen_game = NOBODY
    player_message = "Chose a game to play!"

    def game_choice_function(selected_game):
        '''assassin vote'''
        def callback():
            '''callback'''
            global chosen_game
            chosen_game = selected_game
            global just_voted
            just_voted = True

        return callback

    create_voting_screen(games_list, game_choice_function,
                         player_message=player_message)

    logger.log_debug("Chosen game was " + chosen_game)
    WindowSingleton.destroy_instance()
    return chosen_game


def night_assassin_vote(town_names):
    '''assassin vote'''
    global assassinated_person
    assassinated_person = NOBODY
    player_message = "NIGHT PHASE: Assassins kill: "

    def assassin_vote_function(player_name):
        '''assassin vote'''
        def callback():
            '''callback'''
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
    '''cop vote'''
    global checked_person
    checked_person = NOBODY
    player_message = "NIGHT PHASE: Cop checks: "

    def cop_vote_function(player_name):
        '''cop vote'''
        def callback():
            '''callback'''
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
    '''doctor vote'''
    global saved_person
    saved_person = NOBODY
    player_message = "NIGHT PHASE: Doctor saves: "

    def doctor_vote_function(player_name):
        '''doctor vote'''
        def callback():
            '''callback'''
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
    '''mutilator vote'''
    global mutilated_person, mutilation_place
    mutilated_person = NOBODY
    mutilation_place = NOBODY
    def mutilator_vote_function(player_name):
        '''mutilator vote'''
        def callback():
            '''callback'''
            global mutilated_person
            mutilated_person = player_name
            global just_voted
            just_voted = True

        return callback

    def mutilator_place_function(place_name):
        def callback():
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
        create_voting_screen(["Hand", "Mouth"], mutilator_place_function)

    logger.log_debug("Mutilator targeted " + mutilated_person)
    return (mutilated_person, mutilation_place)

#lista = ["Marcel", "Ionela", "Trump", "Putin", "Altcineva"]
#lista.extend(lista)
#lista.append("DA")
# players_number=get_players_number()
#show_info("hello")
