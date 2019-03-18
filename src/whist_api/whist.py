''' Implementation of a Romanian Whist scoreboard. '''
from whist_api.gamestate_api.gamestate import GameState
import whist_api.io_api.facade_io as io
import whist_api.ui_api.ui as ui

def start():
    ''' Starts a game of Whist. '''
    ui.start_window_thread()
    #print(ui.get_player_bid("Marcel", [0, 1, 2]))
    player_cnt = io.get_player_cnt()
    player_names = io.get_names(player_cnt)
    gamestate = GameState(player_cnt, player_names)
    gamestate.start_game()
