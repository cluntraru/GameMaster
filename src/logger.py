''' Logger implementation. '''
import sys

DEBUG_MODE = None
SPEAK_MODE = None

def set_debug_mode(debug_mode):
    ''' Sets debug mode once. '''
    global DEBUG_MODE
    if DEBUG_MODE is None:
        DEBUG_MODE = debug_mode
    else:
        log_info('Debug mode can only be set once.')
        sys.exit()


def set_speak_mode(speak_mode):
    ''' Sets speak mode once. '''
    global SPEAK_MODE
    if SPEAK_MODE is None:
        SPEAK_MODE = speak_mode
    else:
        log_info('Speak mode can only be set once.')
        sys.exit()


def log_info(text):
    ''' Prints to console. '''
    print(text)


def log_debug(text):
    ''' Logs to console only if debug mode is enabled. '''
    if DEBUG_MODE:
        print(text)


def is_debug_mode():
    ''' Returns if debug mode is enabled. '''
    return DEBUG_MODE


def is_speak_mode():
    ''' Returns if speak mode is enabled. '''
    return SPEAK_MODE
