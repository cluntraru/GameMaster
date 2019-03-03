''' Implementation of a Romanian Whist scoreboard. '''
from argparse import ArgumentParser
from whist_api.gamestate_api.gamestate import GameState
import whist_api.io_api.facade_io as io
from whist_api.io_api.whist_logger import WhistLogger

def start(debug_mode, speak_mode):
    ''' Starts a game of Whist. '''
    logger = WhistLogger(debug_mode, speak_mode)
    player_cnt = io.get_player_cnt(logger)
    player_names = io.get_names(logger, player_cnt)
    gs = GameState(logger, player_cnt, player_names)
    gs.start_game()


if __name__ == '__main__':
    parser = ArgumentParser()
    # Does not have effect here, but we shouldn't break mafia mode
    parser.add_argument('-x', '--textonly', action='store_true',
                        help='Do not use voice output')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='All I/O comes from console')

    args = parser.parse_args()
    start(args.debug, not args.textonly)
