''' Facade for handling input and output. '''
import sys
import os

try:
    import win32com.client
except ModuleNotFoundError:
    pass


import mafia_api.io_api.release_io as rlio
import mafia_api.io_api.debug_io as dbgio
from mafia_api.player_api.player import Player
import logger

SPEAKER = None

def get_player_cnt():
    ''' Prompts for number of players and returns the result. '''
    if logger.is_debug_mode():
        return dbgio.get_player_cnt()

    return rlio.get_player_cnt()


def get_names_emails(role_list, player_cnt, player_data):
    ''' Prompts for player names and emails and returns a pair of arrays. '''
    if logger.is_debug_mode():
        return dbgio.get_names_emails(role_list, player_cnt, player_data)

    return rlio.get_names_emails(role_list, player_cnt, player_data)


def get_lynched_name(can_vote, still_alive):
    ''' Prompts for name of player to lynch. '''
    if logger.is_debug_mode():
        return dbgio.get_lynched_name()

    return rlio.get_lynched_name(can_vote, still_alive)


def get_assn_target(player_data, targets):
    ''' Prompts for assassination target and returns the result. '''
    if logger.is_debug_mode():
        return dbgio.get_assn_target(player_data)

    return rlio.get_assn_target(targets)


def get_police_target(player_data, targets):
    ''' Prompts for police interrogation and returns the chosen person's name.
    '''
    if logger.is_debug_mode():
        return dbgio.get_police_target(player_data)

    return rlio.get_police_target(targets)


def show_police_answer(player_data, target):
    ''' Alerts whether the person interrogated by the police is an assassin or
    not. '''
    if logger.is_debug_mode():
        return dbgio.show_police_answer(player_data, target)

    return rlio.show_police_answer(player_data, target)


def get_mutilator_target(player_data, targets):
    ''' Prompts for mutilatotion target and target area and returns a
    pair. '''
    if logger.is_debug_mode():
        return dbgio.get_mutilator_target(player_data)

    return rlio.get_mutilator_target(targets)


def get_doctor_target(player_data, targets):
    ''' Prompts for doctor target and returns their name. '''
    if logger.is_debug_mode():
        return dbgio.get_doctor_target(player_data)

    return rlio.get_doctor_target(targets)


def _speak(text):
    ''' Wrapper for platform specific text-to-speech functionality. Should be
    called similar to print(). '''
    if sys.platform == 'darwin':
        os.system('say ' + '"' + text + '"')
    elif sys.platform == 'win32':
        global SPEAKER
        if SPEAKER is None:
            SPEAKER = win32com.client.Dispatch("SAPI.SpVoice")

        SPEAKER.Speak(text)


def output(text):
    ''' Speaks and prints the input text if SPEAK_MODE is enabled. Prints
    otherwise. '''
    if logger.is_speak_mode():
        _speak(text)
        logger.log_info(text)
    else:
        logger.log_info(text)


def show_player(player_name, player_data):
    ''' Prints the role and status (dead/alive) of a player. '''
    if player_data[player_name].get_alive():
        status = 'ALIVE'
    else:
        status = 'DEAD'

    logger.log_info(player_name + ' the ' +\
                  player_data[player_name].get_role_name() + ' - ' + status)


def show_mafia(player_data):
    ''' Prints all members of the mafia. '''
    logger.log_info('Mafia:')
    for player_name in player_data:
        if player_data[player_name].get_role_idx() != Player.ASSN_IDX:
            continue

        show_player(player_name, player_data)

    logger.log_info('\n')


def show_town(player_data):
    ''' Prints all members of the town. '''
    logger.log_info('Town:')
    for player_name in player_data:
        if player_data[player_name].get_role_idx() == Player.ASSN_IDX or\
           player_data[player_name].get_role_idx() == Player.SUICD_IDX:

            continue

        show_player(player_name, player_data)

    logger.log_info('\n')


def show_suicidal(player_data):
    ''' Prints the suicidal person. '''
    logger.log_info('Neutral:')
    for player_name in player_data:
        if player_data[player_name].get_role_idx() == Player.SUICD_IDX:
            show_player(player_name, player_data)
            break

    logger.log_info('\n')
