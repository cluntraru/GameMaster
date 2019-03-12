''' Entry point to GameMaster app. '''
from argparse import ArgumentParser
import mafia_api.mafia as mafia
import ui as initial_ui
import whist_api.whist as whist
import logger

if __name__ == '__main__':
    parser = ArgumentParser()
    # Only has effect in mafia
    parser.add_argument('-x', '--textonly', action='store_true',
                        help='Do not use voice output')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='All I/O comes from console')

    ARGS = parser.parse_args()
    logger.set_debug_mode(ARGS.debug)
    logger.set_speak_mode(not ARGS.textonly)

    GAME = initial_ui.game_choice(["mafia", "whist"])
    if GAME == 'mafia':
        mafia.start()
    elif GAME == 'whist':
        whist.start()
