'''Ui of mafia storyteller'''

from tkinter import Frame, Tk, Button, Text, LEFT, BOTTOM, INSERT, Label, Entry
from math import floor

COLORS = ["red", "green", "blue", "brown", "orange", "purple"]
NOBODY = "NONE"
MAX_ENTRIES = 10
LEFT_SHIFT = 300

assassinated_person = NOBODY
checked_person = NOBODY
saved_person = NOBODY
mutilated_person = NOBODY
mutilation_place = NOBODY


def get_emails_form(player_names):
    '''creates and shows email form'''
    curr_window = Tk()
    curr_window.geometry('500x500')
    curr_window.title("Email Form")
    label_0 = Label(curr_window, text="Email Form", width=20, font=("bold", 20))
    label_0.place(x=90, y=53)
    entries = []
    labels = []
    emails = []
    for i in range(0, len(player_names)):
        labels.append(Label(curr_window, text=player_names[i], width=20, font=("bold", 10)))
        labels[i].place(x=80+LEFT_SHIFT*floor(i/MAX_ENTRIES), y=130+30*(i%MAX_ENTRIES))
        entries.append(Entry(curr_window))
        entries[i].place(x=240+LEFT_SHIFT*floor(i/MAX_ENTRIES), y=130+30*(i % MAX_ENTRIES))
        emails.append(("", ""))

    def get_vals():
        '''gets emails from fields'''
        for i in range(0, len(player_names)):
            emails[i] = (player_names[i], entries[i].get())
        curr_window.destroy()

    done_button = Button(curr_window, fg="RED", height=2, width=20, text="Done", command=get_vals)
    done_button.place(x=80+LEFT_SHIFT*floor(len(player_names)/MAX_ENTRIES), y=130+30*(MAX_ENTRIES+1))
    curr_window.mainloop()
    return emails


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

def day_vote(player_names):
    '''day vote'''
    player_votes = {}
    for player_name in player_names:
        player_votes[player_name] = 0
    player_votes[NOBODY] = 0
    for player_name in player_names:

        curr_window = Tk()
        curr_player = player_name
        curr_window.title("DAY PHASE: " + curr_player + " votes ")

        def day_vote_function(player_window, player_name):
            def callback():
                player_votes[player_name] += 1
                player_window.destroy()
            return callback

        create_voting_screen(curr_window, player_names, day_vote_function)


    hanged_player = NOBODY
    for player_name in player_names:
        if player_votes[player_name] > len(player_names) / 2:
            hanged_player = player_name
    print("The victim was: " + hanged_player)
    return hanged_player

def night_assassin_vote(town_names):
    '''assassin vote'''
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

    global assassinated_person
    return assassinated_person

def night_cop_vote(player_names):
    '''cop vote'''
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

    global checked_person
    return checked_person

def night_doctor_vote(player_names):
    '''doctor vote'''
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

    global saved_person
    return saved_person

def night_mutilator_vote(player_names):
    '''mutilator vote'''
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

    curr_window = Tk()
    curr_window.title("NIGHT PHASE: " + "Mutilator mutilates: ")
    create_voting_screen(curr_window, ["Hand", "Mouth"], mutilator_place_function)

    global mutilared_person, mutilation_place
    return (mutilated_person, mutilation_place)

#lista = ["Marcel", "Ionela", "Trump", "Putin", "Atcineva"]
#lista.extend(lista)
#lista.append("DA")
#get_emails_form(lista)
#show_info("hello")
