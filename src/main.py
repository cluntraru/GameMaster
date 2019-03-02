import mafia_api.mafia as mafia
import whist_api.whist as whist
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    # Only has effect in mafia
    parser.add_argument('-x', '--textonly', action='store_true',
                        help='Do not use voice output')

    parser.add_argument('-d', '--debug', action='store_true',
                        help='All I/O comes from console')

    args = parser.parse_args()

    game = input('Do you want to play whist or mafia?')
    if game == 'mafia':
        mafia.start(args.debug, not args.textonly)
    elif game == 'whist':
        whist.start(args.debug, not args.textonly)
