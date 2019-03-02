''' This deals with all the output '''
import sys
import os
try:
    import win32com.client
except ImportError:
    pass

from mafia_api.player_api.player import Player
from logger import Logger

class MafiaLogger(Logger):
    SPEAKER = None

    def __init__(self, debug_mode, speak_mode):
        super().__init__(debug_mode, speak_mode)
        if sys.platform == 'win32' and Logger.SPEAK_MODE:
            SPEAKER = win32com.client.Dispatch("SAPI.SpVoice")


    def speak(self, text):
        ''' Wrapper for platform specific text-to-speech functionality. Should be
        called similar to print().
        '''
        if sys.platform == 'darwin':
            os.system('say ' + '"' + text + '"')
        elif sys.platform == 'win32':
            SPEAKER.Speak(text)


    def output(self, text):
        ''' Speaks and prints the input text if SPEAK_MODE is enabled. Prints
        otherwise
        '''
        if Logger.SPEAK_MODE:
            self.speak(text)
            self.log_info(text)
        else:
            self.log_info(text)


    def log_player(self, player_name, player_data):
        ''' Prints the role and status (dead/alive) of a player. '''
        if player_data[player_name].get_alive():
            status = 'ALIVE'
        else:
            status = 'DEAD'

        self.log_info(player_name + ' the ' +\
                 player_data[player_name].get_role_name() + ' - ' + status)


    def log_mafia(self, player_data):
        ''' Prints all members of the mafia. '''
        self.log_info('Mafia:')
        for player_name in player_data:
            if player_data[player_name].get_role_idx() != Player.ASSN_IDX:
                continue

            self.log_player(player_name, player_data)

        self.log_info('\n')


    def log_town(self, player_data):
        ''' Prints all members of the town. '''
        self.log_info('Town:')
        for player_name in player_data:
            if player_data[player_name].get_role_idx() == Player.ASSN_IDX or\
               player_data[player_name].get_role_idx() == Player.SUICD_IDX:

                continue

            self.log_player(player_name, player_data)

        self.log_info('\n')


    def log_suicidal(self, player_data):
        ''' Prints the suicidal person. '''
        self.log_info('Neutral:')
        for player_name in player_data:
            if player_data[player_name].get_role_idx() == Player.SUICD_IDX:
                self.log_player(player_name, player_data)
                break

        self.log_info('\n')


    def dbg_log_all_roles(self, player_data):
        ''' Prints all roles in debug mode. '''
        for player_name in player_data:
            self.log_debug(player_name + ' the ' + player_data[player_name].get_role_name() + '.')
