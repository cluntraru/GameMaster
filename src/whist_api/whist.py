import whist_api.gamestate_api.gamestate as gs
import whist_api.io_api.facade_io as io
from logger import Logger

def start(debug_mode, speak_mode):
    logger = Logger(debug_mode, speak_mode)
    player_cnt = io.get_player_cnt(logger)
    player_names =  io.get_names(logger, player_cnt)
    gamestate = gs.GameState(logger, player_cnt, player_names);


if __name__ == '__main__':
    parser = ArgumentParser()
    # Does not have effect here, but we shouldn't break mafia mode
    parser.add_argument('-x', '--textonly', action='store_true',
                        help='Do not use voice output')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='All I/O comes from console')

    args = parser.parse_args()
    start(args.debug, not args.textonly)
