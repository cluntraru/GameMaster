''' Implementation of a Romanian Whist scoreboard. '''
from argparse import ArgumentParser
from whist_api.gamestate_api.gamestate import GameState
import whist_api.io_api.facade_io as io
import logger

def start():
    ''' Starts a game of Whist. '''
    player_cnt = io.get_player_cnt()
    player_names = io.get_names(player_cnt)
    gs = GameState(player_cnt, player_names)
    gs.start_game()


if __name__ == '__main__':
    parser = ArgumentParser()
    # Does not have effect here, but we shouldn't break mafia mode
    parser.add_argument('-x', '--textonly', action='store_true',
                        help='Do not use voice output')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='All I/O comes from console')

    ARGS = parser.parse_args()

    logger.set_debug_mode(ARGS.debug)
    logger.set_speak_mode(not ARGS.textonly)

    start()
