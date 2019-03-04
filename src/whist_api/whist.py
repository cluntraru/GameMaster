''' Implementation of a Romanian Whist scoreboard. '''
from whist_api.gamestate_api.gamestate import GameState
import whist_api.io_api.facade_io as io

def start():
    ''' Starts a game of Whist. '''
    player_cnt = io.get_player_cnt()
    player_names = io.get_names(player_cnt)
    gamestate = GameState(player_cnt, player_names)
    gamestate.start_game()
