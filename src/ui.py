"""UI for choosing games"""
from tkinter import Frame, Tk, Button, LEFT, Label
import logger

COLORS = ["green", "blue", "yellow", "orange", "purple", "brown"]
NOBODY = "NONE"
MAX_ENTRIES = 10
LEFT_SHIFT = 160
FIELD_SPACE = 40
TITLE_SPACE = 200
chosen_game = NOBODY
just_voted = False

def create_voting_screen(player_names, vote_function, player_message="Time to vote"):
    '''screen populating function'''
    player_window = Tk()

    background_color = "white"
    player_window.configure(background=background_color)
    player_window.title(player_message)

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
                             command=vote_function(player_window, player_name))
        vote_button.configure(font=("Courier", 10))
        vote_button.pack(side=LEFT)
    player_window.mainloop()
    #logger.log_debug("Voting screen closed")

def game_choice(games_list):
    '''Game choice'''
    global chosen_game
    chosen_game = NOBODY
    player_message = "Chose a game to play!"

    def game_choice_function(player_window, selected_game):
        '''assassin vote'''
        def callback():
            '''callback'''
            global chosen_game
            chosen_game = selected_game
            global just_voted
            just_voted = True
            player_window.destroy()

        return callback

    create_voting_screen(games_list, game_choice_function,
                         player_message=player_message)

    logger.log_debug("Chosen game was " + chosen_game)
    return chosen_game
