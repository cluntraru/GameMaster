'''Ui of mafia storyteller'''
from tkinter import Frame, Tk, Button, Text, LEFT, TOP, N, INSERT, Label, Entry
from math import floor
import logger
import sys
from threading import Thread, Lock

COLORS = ["green", "blue", "yellow", "orange", "purple", "brown"]
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
log_history = "GAME LOGS: "
field_number = "-1"
just_voted = False
window_open = False

def add_to_log_history(new_logs):
    global log_history
    log_history = log_history + "\n" + new_logs;

def reset_log_history():
    global log_history
    log_history = "GAME LOGS: "


def delete_children(window):
    _list = window.winfo_children()

    for item in _list:
        item.destroy()


get_instance_guard = Lock()

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
    window_open = True
    window.mainloop()
    window_open = False
    #print("Exiting")
    sys.exit()


window_thread = Thread(target=window_thread_start)
window_thread.start()


def get_players_number():
    '''gets players number'''

    background_color = "#A3D9FF"
    foreground_color = "orange"

    add_to_log_history("")
    curr_window = WindowSingleton.get_instance().window
    curr_window.geometry('500x500')
    curr_window.title("Players number")
    curr_window.configure(background=background_color)

    title_text_label = Label(curr_window, text="Welcome to Mafia", width=20, font=("bold", 30))
    #title_text_label.configure(anchor="n")
    title_text_label.place(x=400, y=30, anchor="w")
    title_text_label.configure(background=background_color, foreground=foreground_color)

    form_text_label = Label(curr_window, text="Insert number of players:",
                            width=20, font=("bold", 10))
    form_text_label.place(x=10, y=TITLE_SPACE)
    form_text_label.configure(background=background_color, foreground=foreground_color)

    number_entry = Entry(curr_window)
    number_entry.place(x=20, width=20, y=TITLE_SPACE+FIELD_SPACE)

    def get_val():
        """gets number from field"""
        global field_number

        field_number = number_entry.get()
        if int(field_number) <= 4:
            form_text_label['text'] = "Too few players"
        elif int(field_number) > 20:
            form_text_label['text'] = "Too many players"

    done_button = Button(curr_window, fg="RED", height=0, width=20, text="Done", command=get_val)
    done_button.place(x=20, y=TITLE_SPACE+FIELD_SPACE * 2)
    done_button.configure(background="red", foreground="white")

    if (int(field_number)) == -1:
        logger.log_debug("Window for getting players number closed\n")
    else:
        logger.log_debug("Number of player: " + field_number)
    while (not (4 < int(field_number) <= 20 ) and window_open):
        pass
    WindowSingleton.reset_instance()
    return int(field_number)


def get_emails_form(players_number):
    '''creates and shows email form'''
    background_color = "#A3D9FF"
    foreground_color = "orange"
    curr_window = WindowSingleton.get_instance().window
    curr_window.geometry('500x500')
    curr_window.title("Email form")
    curr_window.configure(background=background_color)
    text_label = Label(curr_window, text="Insert players emails and names",
                       width=40, font=("bold", 20), anchor="w")
    text_label.place(x=380, y=53)
    text_label.configure(background=background_color, foreground=foreground_color)

    entries = []
    labels = []
    emails_and_names = []
    for i in range(0, players_number):
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

    def check_different_names():
        different_names = True
        nonlocal emails_and_names
        players_number = len(emails_and_names)
        for i in range(0, players_number):
            for j in range(0, players_number):
                if i != j:
                    if emails_and_names[i][0] == emails_and_names[j][0]:
                        different_names = False
        return different_names

    def check_empty_names():
        nonempty_names = True
        nonlocal emails_and_names
        players_number = len(emails_and_names)
        if(len(emails_and_names) == 0):
            return False
        for i in range(0, players_number):
            if emails_and_names[i][0] == "":
                nonempty_names = False
        return nonempty_names

    def get_vals():
        '''gets emails from fields'''
        nonlocal emails_and_names
        emails_and_names = []
        for i in range(0, players_number):
            emails_and_names.append((entries[i*2].get(), entries[i * 2 + 1].get()))
        different_names = check_different_names()
        nonempty_names = check_empty_names()

        if different_names and nonempty_names:
            pass
        elif nonempty_names is False:
            text_label['text'] = "One or more names are empty"
        elif different_names is False:
            text_label['text'] = "Two or more names are identical"

    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=get_vals)
    done_button.configure(background="red", foreground="white")
    done_button.place(x=20, y=130+35*(MAX_ENTRIES+1))

    while (not (check_empty_names() and check_different_names())) and window_open:
        pass
        #logger.log_debug("Window for emails and names was closed\n")
    WindowSingleton.reset_instance()
    return emails_and_names


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

def create_voting_screen(player_names, vote_function, player_message="Time to vote"):
    '''screen populating function'''
    global window_open
    while window_open is False:
        pass
    player_window = WindowSingleton.get_instance().window

    background_color = "black"
    player_window.configure(background=background_color)
    player_window.title(player_message)
    logs_frame = Frame(player_window)
    if player_message != "Chose a game to play!":
        logs_frame.pack(side=LEFT)
    global log_history
    logs_label = Label(logs_frame, text=log_history, height=60, width=20,
                       font=("bold", 10), background="blue", anchor=N)
    logs_label.configure(background="purple", foreground="white")
    logs_label.pack(side=TOP)

    game_frame = Frame(player_window)
    game_frame.configure(background=background_color)
    game_frame.pack(side=LEFT)

    title_frame = Frame(game_frame)
    title_frame.configure(background=background_color)
    title_frame.pack()
    text_label = Label(title_frame, text=player_message, width=40,
                       font=("bold", 20), anchor="w", justify="center")
    text_label.configure(background="red")
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
        vote_button = Button(curr_frame, fg="black", background=COLORS[i % len(COLORS)],
                             height=20, width=17, text=player_name,
                             command=vote_function(player_name))
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
        curr_window = WindowSingleton.get_instance().window
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
    curr_window = WindowSingleton.get_instance().window
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
    return chosen_game


def night_assassin_vote(town_names):
    '''assassin vote'''
    global assassinated_person
    assassinated_person = NOBODY
    curr_window = WindowSingleton.get_instance().window
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
    curr_window = WindowSingleton.get_instance().window
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
    curr_window = WindowSingleton.get_instance().window
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

    curr_window = WindowSingleton.get_instance().window
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