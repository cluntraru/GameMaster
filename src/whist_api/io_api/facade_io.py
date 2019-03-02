''' Facade for handling input and output. '''
import whist_api.io_api.release_io as rlio
import whist_api.io_api.debug_io as dbgio

def get_player_cnt(logger):
    ''' Prompts for number of players and returns the result. '''
    if logger.is_debug_mode():
        return dbgio.get_player_cnt()

    return rlio.get_player_cnt()


def get_names(logger, player_cnt):
    ''' Prompts for player names and returns an array. '''
    if logger.is_debug_mode():
        return dbgio.get_names(player_cnt)

    return rlio.get_names(player_cnt)


def show_scoreboard(logger, layer_cnt, player_names, round, scoreboard, diffs):
    if logger.is_debug_mode():
        dbgio.show_scoreboard(player_cnt, player_names, round, scoreboard, diffs)
    else:
        rlio.show_scoreboard(player_cnt, player_names, round, scoreboard, diffs)