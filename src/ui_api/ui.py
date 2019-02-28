'''Ui of mafia storyteller'''
from tkinter import Frame, Tk, Button, Text, LEFT, BOTTOM, INSERT, Label, Entry
from math import floor
import io_api.logger as logger

COLORS = ["red", "green", "blue", "brown", "orange", "purple"]
NOBODY = "NONE"
MAX_ENTRIES = 10
LEFT_SHIFT = 160
UP_SHIFT = 40

assassinated_person = NOBODY
checked_person = NOBODY
saved_person = NOBODY
mutilated_person = NOBODY
mutilation_place = NOBODY
field_number = "-1"

def get_players_number():
    '''gets players number'''
    curr_window = Tk()
    curr_window.geometry('500x500')
    curr_window.title("Players number")

    text_label = Label(curr_window, text="Insert number of players:", width=20, font=("bold",10))
    text_label.place(x = 10, y = UP_SHIFT)
    number_entry = Entry(curr_window)
    number_entry.place(x = 20, y = UP_SHIFT * 2)
    def get_val():
        '''gets number from field'''
        global field_number
        field_number = number_entry.get()
        if int(field_number) <= 4:
            text_label['text'] = "Too few players"
        elif int(field_number) > 20:
            text_label['text'] = "Too many players"
        else:
            curr_window.destroy()
    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=get_val)
    done_button.place(x = 20, y = UP_SHIFT * 3)
    curr_window.mainloop()
    if (int(field_number)) == -1:
        logger.log_debug("Window for getting players number closed\n")
    else:
        logger.log_debug("Number of player: " + field_number)
    return int(field_number)


def get_emails_form(players_number):
    '''creates and shows email form'''
    curr_window = Tk()
    curr_window.geometry('500x500')
    curr_window.title("Email Form")
    text_label = Label(curr_window, text="Email Form", width=40, font=("bold", 20))
    text_label.place(x=90, y=53)
    entries = []
    labels = []
    emails_and_names = []
    for i in range(0, players_number):
        labels.append(Label(curr_window, text="Player " + str(i + 1) + " name:", width=20, font=("bold", 10)))
        labels[i*2].place(x=LEFT_SHIFT*4*floor(i/MAX_ENTRIES), y=130+30*(i%MAX_ENTRIES))
        entries.append(Entry(curr_window))
        entries[i*2].place(x=LEFT_SHIFT*(4*(floor(i/MAX_ENTRIES))+1), y=130+30*(i % MAX_ENTRIES))

        labels.append(Label(curr_window, text="Player " + str(i + 1) + " email:", width=20, font=("bold", 10)))
        labels[i * 2 + 1].place(x=LEFT_SHIFT * (4 * floor(i / MAX_ENTRIES) + 2), y=130 + 30 * (i % MAX_ENTRIES))
        entries.append(Entry(curr_window))
        entries[i * 2 +1].place(x=LEFT_SHIFT * (4 * floor(i / MAX_ENTRIES) + 3), y=130 + 30 * (i % MAX_ENTRIES))
    logger.log_debug("Created email fields")
    def check_different_names():
        different_names = True
        nonlocal emails_and_names
        for i in range(0,players_number):
            for j in range(0,players_number):
                if i!=j:
                    if(emails_and_names[i][0] == emails_and_names[j][0]):
                        different_names = False
        return different_names

    def check_empty_names():
        nonempty_names = True
        nonlocal emails_and_names
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
            curr_window.destroy()
        elif nonempty_names == False:
            text_label['text'] = "One or more names are empty"
        elif different_names == False:
            text_label['text'] = "Two or more names are identical"

    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=get_vals)
    done_button.place(x=80+LEFT_SHIFT*floor(players_number/MAX_ENTRIES), y=130+30*(MAX_ENTRIES+1))
    curr_window.mainloop()
    if(len(emails_and_names) == 0):
        logger.log_debug("Window for emails and names was closed\n")
    return emails_and_names


def show_info(curr_info):
    '''shows info, mostly for cop'''
    curr_window = Tk()
    curr_window.title("Night Report For Cop")
    def destroy_window():
        '''destroys window'''
        curr_window.destroy()

    screen_info = Text(curr_window)
    screen_info.insert(INSERT, curr_info)
    screen_info.pack()
    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=destroy_window)
    done_button.pack()
    curr_window.mainloop()
    logger.log_debug("Info window closed")

def create_voting_screen(player_window, player_names, vote_function): #populates all voting screens
    '''screen populating function'''
    top_frame = Frame(player_window)
    top_frame.pack()

    bottom_frame = Frame(player_window)
    bottom_frame.pack()

    number_of_players = len(player_names)
    for i in range(0, number_of_players):
        player_name = player_names[i]
        if i < number_of_players / 2:
            curr_frame = top_frame
        else:
            curr_frame = bottom_frame
        done_button = Button(curr_frame, fg=COLORS[i % len(COLORS)], height=20, width=17, text=player_name, command=vote_function(player_window, player_name))
        done_button.pack(side=LEFT)

    player_window.mainloop()  # make sure buttons are constantly displayed
    logger.log_debug("Voting screen closed")


def day_vote(players_can_vote, votable_players):
    '''day vote'''
    player_votes = {}
    for player_name in votable_players:
        player_votes[player_name] = 0
    player_votes[NOBODY] = 0
    for player_name in players_can_vote:
        curr_window = Tk()
        curr_player = player_name
        curr_window.title("DAY PHASE: " + curr_player + " votes ")

        def day_vote_function(player_window, player_name):
            def callback():
                player_votes[player_name] += 1
                player_window.destroy()
            return callback

        create_voting_screen(curr_window, votable_players, day_vote_function)

    hanged_player = NOBODY
    for player_name in votable_players:
        if player_votes[player_name] > len(votable_players) / 2:
            hanged_player = player_name
    logger.log_debug("The day victim was: " + hanged_player)
    return hanged_player


def night_assassin_vote(town_names):
    '''assassin vote'''
    global assassinated_person
    assassinated_person = NOBODY
    curr_window = Tk()
    curr_window.title("NIGHT PHASE: " +  "Assassins kill: ")

    def assassin_vote_function(player_window, player_name):
        '''assassin vote'''
        def callback():
            '''callback'''
            global assassinated_person
            assassinated_person = player_name
            player_window.destroy()

        return callback

    create_voting_screen(curr_window, town_names, assassin_vote_function)

    logger.log_debug("Night victim was " + assassinated_person)
    return assassinated_person


def night_cop_vote(player_names):
    '''cop vote'''
    global checked_person
    checked_person = NOBODY
    curr_window = Tk()
    curr_window.title("NIGHT PHASE: " +  "Cop checks: ")

    def cop_vote_function(player_window, player_name):
        '''cop vote'''
        def callback():
            '''callback'''
            global checked_person
            checked_person = player_name
            player_window.destroy()

        return callback

    create_voting_screen(curr_window, player_names, cop_vote_function)

    logger.log_debug("Cop checked " + checked_person)
    return checked_person


def night_doctor_vote(player_names):
    '''doctor vote'''
    global saved_person
    saved_person = NOBODY
    curr_window = Tk()
    curr_window.title("NIGHT PHASE: " +  "Doctor saves: ")

    def doctor_vote_function(player_window, player_name):
        '''doctor vote'''
        def callback():
            '''callback'''
            global saved_person
            saved_person = player_name
            player_window.destroy()

        return callback

    create_voting_screen(curr_window, player_names, doctor_vote_function)

    logger.log_debug("Doctor saved " + saved_person)
    return saved_person


def night_mutilator_vote(player_names):
    '''mutilator vote'''
    global mutilated_person,mutilation_place
    mutilated_person = NOBODY
    mutilation_place = NOBODY
    def mutilator_vote_function(player_window, player_name):
        '''mutilator vote'''
        def callback():
            '''callback'''
            global mutilated_person
            mutilated_person = player_name
            player_window.destroy()

        return callback

    def mutilator_place_function(player_window, place_name):
        def callback():
            global mutilation_place
            mutilation_place = place_name[0]
            player_window.destroy()

        return callback

    curr_window = Tk()
    curr_window.title("NIGHT PHASE: " + "Mutilator mutilates: ")
    create_voting_screen(curr_window, player_names, mutilator_vote_function)

    if mutilated_person != NOBODY:
        curr_window = Tk()
        curr_window.title("NIGHT PHASE: " + "Mutilator mutilates: ")
        create_voting_screen(curr_window, ["Hand", "Mouth"], mutilator_place_function)

    logger.log_debug("Mutilator targeted " + mutilated_person)
    return (mutilated_person, mutilation_place)

#lista = ["Marcel", "Ionela", "Trump", "Putin", "Atcineva"]
#lista.extend(lista)
#lista.append("DA")
# players_number=get_players_number()
# print(get_emails_form(5))
#show_info("hello")
