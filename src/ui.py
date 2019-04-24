"""UI for choosing games"""
from tkinter import Frame, Tk, Button, LEFT, TOP, Label
import logger

NOBODY = "NONE"
MAX_ENTRIES = 10
LEFT_SHIFT = 160
FIELD_SPACE = 40
TITLE_SPACE = 200
chosen_game = NOBODY
just_voted = False

ANTI_FLASH_WHITE = "#F0F2EF"
UMBER = "#5C5346"
SPICY_MIX = "#8C6057"
LIGHT_MOSS_GREEN = "#AFD5AA"


def create_voting_screen(player_names, vote_function, player_message="Time to vote"):
    '''Creates a window in which the player can vote'''
    player_window = Tk()
    width_value = player_window.winfo_screenwidth()
    height_value = player_window.winfo_screenheight()
    player_window.geometry("%dx%d+0+0" % (width_value, height_value))
    background_color = ANTI_FLASH_WHITE
    player_window.configure(background=background_color)
    player_window.title(player_message)

    game_frame = Frame(player_window)
    game_frame.configure(background=background_color)
    game_frame.pack(side=TOP)

    title_frame = Frame(game_frame)
    title_frame.configure(background=background_color)
    title_frame.pack()
    text_label = Label(title_frame, text=player_message, width=width_value,
                       font=("bold", 20), anchor="w", justify="center")
    text_label.configure(bg=UMBER, fg=ANTI_FLASH_WHITE)
    text_label.pack(side=TOP)

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
        vote_button = Button(curr_frame, bg=SPICY_MIX, fg=ANTI_FLASH_WHITE,
                             height=20, width=17, text=player_name,
                             command=vote_function(player_window, player_name))
        vote_button.configure(font=("Courier", 10))
        vote_button.pack(side=LEFT)
    player_window.mainloop()
    #logger.log_debug("Voting screen closed")

def game_choice(games_list):
    '''Creates a window in which the player can choose the game he wants to play'''
    global chosen_game
    chosen_game = NOBODY
    player_message = "Chose a game to play!"

    def game_choice_function(player_window, selected_game):
        '''returns the function called when the player chooses a game'''
        def callback():
            '''function called when the player chooses a game'''
            global chosen_game, just_voted
            chosen_game = selected_game
            just_voted = True
            player_window.destroy()

        return callback

    create_voting_screen(games_list, game_choice_function,
                         player_message=player_message)

    logger.log_debug("Chosen game was " + chosen_game)
    return chosen_game
