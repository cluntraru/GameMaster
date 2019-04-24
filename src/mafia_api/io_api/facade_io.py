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

def add_logs(text):
    '''Adds logs in ui'''
    if logger.is_debug_mode():
        print(text)
    else:
        rlio.add_logs(text)

def reset_logs():
    '''Resets logs in ui'''
    if logger.is_debug_mode():
        print("Logs reseted\n")
    else:
        rlio.reset_logs()


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
        #logger.log_info(text)
    else:
        logger.log_info(text)


def show_player(player_name, player_data):
    ''' Returns logs of the role and status (dead/alive) of a player. '''
    if player_data[player_name].get_alive():
        status = 'ALIVE'
    else:
        status = 'DEAD'

    return str(player_name + ' the ' +\
                  player_data[player_name].get_role_name() + ' - ' + status)


def show_mafia(player_data):
    ''' Returns logs of all members of the mafia. '''
    curr_logs = ''
    curr_logs = curr_logs + 'Mafia: \n'
    for player_name in player_data:
        if player_data[player_name].get_role_idx() != Player.ASSN_IDX:
            continue

        curr_logs += show_player(player_name, player_data) + '\n'

    curr_logs += '\n'
    return curr_logs


def show_town(player_data):
    ''' Returns logs of all members of the town. '''
    curr_logs = ''
    curr_logs += 'Town: \n'
    for player_name in player_data:
        if player_data[player_name].get_role_idx() == Player.ASSN_IDX or\
           player_data[player_name].get_role_idx() == Player.SUICD_IDX:

            continue

        curr_logs += show_player(player_name, player_data) + '\n'

    curr_logs += '\n'
    return curr_logs


def show_suicidal(player_data):
    ''' Returns logs of the suicidal person. '''
    curr_logs = ''
    curr_logs += 'Neutral: \n'
    for player_name in player_data:
        if player_data[player_name].get_role_idx() == Player.SUICD_IDX:
            curr_logs += show_player(player_name, player_data) + '\n'
            break

    curr_logs += '\n'
    return curr_logs

def show_results(result, player_data):
    '''Gets all the game logs and shows them'''
    game_logs = result + '\n\n'
    game_logs += show_mafia(player_data)
    game_logs += show_town(player_data)
    game_logs += show_suicidal(player_data)
    if logger.is_debug_mode():
        logger.log_info(game_logs)
    else:
        rlio.show_game_logs(game_logs)
