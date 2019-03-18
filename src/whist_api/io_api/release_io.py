import whist_api.ui_api.ui as ui

def get_player_cnt():
    return ui.get_players_number()


def get_names(player_cnt):
    return ui.get_names_form(player_cnt)


def get_bid(name, possible_bids):
    return ui.get_player_number_input(name, possible_bids, "bid")


def get_result(name, possible_results):
    return ui.get_player_number_input(name, possible_results, "result")


def show_scoreboard(player_cnt, player_names, target_round, scoreboard, diffs):
    ui.show_scoreboard(player_names, target_round, scoreboard)
