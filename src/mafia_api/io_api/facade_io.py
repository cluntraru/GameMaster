''' Facade for handling input and output. '''
import mafia_api.io_api.release_io as rlio
import mafia_api.io_api.debug_io as dbgio
# from mafia.io_api.mafia_logger import MafiaLogger as Logger

def get_player_cnt(logger):
    ''' Prompts for number of players and returns the result. '''
    if logger.is_debug_mode():
        return dbgio.get_player_cnt()

    return rlio.get_player_cnt(logger)


def get_names_emails(logger, role_list, player_cnt, player_data):
    ''' Prompts for player names and emails and returns a pair of arrays. '''
    if logger.is_debug_mode():
        return dbgio.get_names_emails(role_list, player_cnt, player_data)

    return rlio.get_names_emails(logger, role_list, player_cnt, player_data)


def get_lynched_name(logger, can_vote, still_alive):
    ''' Prompts for name of player to lynch. '''
    if logger.is_debug_mode():
        return dbgio.get_lynched_name()

    return rlio.get_lynched_name(logger, can_vote, still_alive)


def get_assn_target(logger, player_data, targets):
    ''' Prompts for assassination target and returns the result. '''
    if logger.is_debug_mode():
        return dbgio.get_assn_target(player_data)

    return rlio.get_assn_target(logger, targets)


def get_police_target(logger, player_data, targets):
    ''' Prompts for police interrogation and returns the chosen person's name.
    '''
    if logger.is_debug_mode():
        return dbgio.get_police_target(player_data)

    return rlio.get_police_target(logger, targets)


def show_police_answer(logger, player_data, target):
    ''' Alerts whether the person interrogated by the police is an assassin or
    not. '''
    if logger.is_debug_mode():
        return dbgio.show_police_answer(logger, player_data, target)

    return rlio.show_police_answer(logger, player_data, target)


def get_mutilator_target(logger, player_data, targets):
    ''' Prompts for mutilatotion target and target area and returns a
    pair. '''
    if logger.is_debug_mode():
        return dbgio.get_mutilator_target(player_data)

    return rlio.get_mutilator_target(logger, targets)


def get_doctor_target(logger, player_data, targets):
    ''' Prompts for doctor target and returns their name. '''
    if logger.is_debug_mode():
        return dbgio.get_doctor_target(player_data)

    return rlio.get_doctor_target(logger, targets)
