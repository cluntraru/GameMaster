import pprint

def get_player_cnt():
    ''' Console prompts for number of players. '''
    return int(input('Enter number of players: '))


def get_names(player_cnt):
    ''' Console prompts for player names. '''
    print('Please enter your names in a circular, clockwise order.')
    names = []
    for i in range(player_cnt):
        curr_name = input('Enter player ' + str(i + 1) + ' name: ')
        while curr_name == '':
            curr_name = input('Enter player ' + str(i + 1) + ' name: ')

        names.append(curr_name)

    return names


def show_scoreboard(logger, player_cnt, player_names, round, scoreboard, diffs):
    ''' Prints scoreboard in console. '''
    logger.log_info('Scoreboard')
    logger.log_info(player_names)
    logger.log_info(scoreboard)
