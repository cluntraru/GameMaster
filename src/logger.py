''' This deals with all the output '''
import sys
import constants as ct
import os
try:
    import win32com.client
except ImportError:
    pass

DEBUG_MODE = None
SPEAK_MODE = None

SPEAKER = None

def win32_speak_init():
    ''' Initialize Windows TTS. '''
    global SPEAKER
    if SPEAKER == None:
        SPEAKER = win32com.client.Dispatch("SAPI.SpVoice")


def speak(text):
    ''' Wrapper for platform specific text-to-speech functionality. Should be
    called similar to print().
    '''
    # TODO: (Chris) add text-to-speech for Windows and Linux
    if sys.platform == 'darwin':
        os.system('say ' + '"' + text + '"')
    elif sys.platform == 'win32':
        win32_speak_init()
        SPEAKER.Speak(text)


def log_info(text):
    ''' Prints information to console. '''
    print(text)


def log_debug(text):
    ''' Prints information to console if debug mode is enabled. '''    
    if DEBUG_MODE:
        print(text)


def output(text):
    ''' Speaks and prints the input text if SPEAK_MODE is enabled. Prints
    otherwise
    '''
    if SPEAK_MODE:
        speak(text)
        log_info(text)
    else:
        log_info(text)


def set_debug_mode(debug_mode):
    ''' Sets speak mode ONCE. '''
    global DEBUG_MODE
    if DEBUG_MODE == None:
        DEBUG_MODE = debug_mode
    else:
        log_debug('Attempt to set debug mode more than once.')
        sys.exit()


def set_speak_mode(speak_mode):
    ''' Sets debug mode ONCE. '''
    global SPEAK_MODE
    if SPEAK_MODE == None:
        SPEAK_MODE = speak_mode
    else:
        log_debug('Attempt to set speak mode more than once.')
        sys.exit()


def is_debug_mode():
    ''' Returns if debug mode is enabled. '''
    return DEBUG_MODE


def is_speak_mode():
    ''' Returns if speak mode is enabled. '''
    return SPEAK_MODE


def log_player(player_name, player_data):
    ''' Prints the role and status (dead/alive) of a player. '''
    if player_data[player_name].get_alive():
        status = 'ALIVE'
    else:
        status = 'DEAD'

    log_info(player_name + ' the ' +\
             player_data[player_name].get_role_name() + ' - ' + status)


def log_mafia(player_data):
    ''' Prints all members of the mafia. '''
    log_info('Mafia:')
    for player_name in player_data:
        if player_data[player_name].get_role_idx() != ct.ASSN_IDX:
            continue

        log_player(player_name, player_data)

    log_info('\n')


def log_town(player_data):
    ''' Prints all members of the town. '''
    log_info('Town:')
    for player_name in player_data:
        if player_data[player_name].get_role_idx() == ct.ASSN_IDX or\
           player_data[player_name].get_role_idx() == ct.SUICD_IDX:
           
            continue

        log_player(player_name, player_data)

    log_info('\n')


def log_suicidal(player_data):
    ''' Prints the suicidal person. '''
    log_info('Neutral:')
    for player_name in player_data:
        if player_data[player_name].get_role_idx() == ct.SUICD_IDX:
            log_player(player_name, player_data)
            break

    log_info('\n')


def dbg_log_all_roles(player_data):
    for player_name in player_data:
        log_debug(player_name + ' the ' + player_data[player_name].get_role_name() + '.')
