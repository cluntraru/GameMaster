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


def get_bid(logger, name, possible_bids):
    ''' Prompts a player for their bid. '''
    if logger.is_debug_mode():
        return dbgio.get_bid(name, possible_bids)

    return rlio.get_bid()


def get_result(logger, name, possible_results):
    ''' Prompts a player for their result that round. '''
    if logger.is_debug_mode():
        return dbgio.get_result(name, possible_results)

    return rlio.get_result()


def show_scoreboard(logger, player_cnt, player_names, target_round, scoreboard, diffs):
    ''' Shows players the scoreboard.  '''
    if logger.is_debug_mode():
        dbgio.show_scoreboard(logger, player_cnt, player_names, target_round, scoreboard, diffs)
    else:
        rlio.show_scoreboard(logger, player_cnt, player_names, target_round, scoreboard, diffs)
