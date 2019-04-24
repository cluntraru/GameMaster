''' Functions that get input from UI. '''
import whist_api.ui_api.ui as ui

def get_player_cnt():
    '''Prompts window to get number of players'''
    return ui.get_players_number()


def get_names(player_cnt):
    '''Prompts window to get the names of the players'''
    return ui.get_names_form(player_cnt)


def get_bid(name, possible_bids):
    '''Prompts window to get a bid'''
    return ui.get_player_number_input(name, possible_bids, "bid")


def get_result(name, possible_results):
    '''Prompts window to get a result'''
    return ui.get_player_number_input(name, possible_results, "result")


def show_scoreboard(player_cnt, player_names, target_round, scoreboard, diffs):
    '''Prompts window to show scoreboard'''
    ui.show_scoreboard(player_names, target_round, scoreboard)
