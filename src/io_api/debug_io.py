''' Functions that ask for input from console. '''
import random
import io_api.logger as logger
import player_api.player as pl
import email_api.gm_email as email

def get_player_cnt():
    return int(input('Enter number of players: '))


def get_names_emails(role_list, player_cnt, player_data):
    emails = []
    msgs = []
    for i in range(player_cnt):
        curr_name = input('Enter player ' + str(i + 1) + ' name: ')
        while (curr_name == '' or curr_name in player_data):
            curr_name = input('Please choose another name: ')

        curr_email = input('Enter player ' + str(i + 1) + ' e-mail: ')

        rand_index = random.randint(0, len(role_list) - 1)
        player_data[curr_name] = pl.Player(role_list.pop(rand_index))

        curr_msg = email.get_msg_from_name(curr_name, player_data)

        emails.append(curr_email)
        msgs.append(curr_msg)

    return emails, msgs


def get_lynched_name():
    return input('Name of lynched player: ')


def _valid_target(player_name, player_data):
    ''' Checks if a player is in the game and alive. '''
    return player_name in player_data and player_data[player_name].get_alive()


def get_assn_target(player_data):
    assassinated = input('Person to assassinate: ')
    while not _valid_target(assassinated, player_data) or\
          player_data[assassinated].is_assn():

        assassinated = input('Invalid target. Person to assassinate: ')

    return assassinated


def get_police_target(player_data):
    police_query = input('Person to query: ')
    while not _valid_target(police_query, player_data):
        police_query = input('Invalid target. Person to query: ')


def show_police_answer(player_data, target):
    if player_data[target].is_assn():
        logger.log_info('The person you queried is an assassin.\n')
    elif police_query:
        logger.log_info('The person you queried is NOT an assassin.\n')    


def get_mutilator_target(player_data):
    mutilated = input('Person to mutilate: ')
    while not _valid_target(mutilated, player_data):
        mutilated = input('Invalid target. Person to mutilate: ')

    mutilated_area = input('Area to mutilate (M/H): ')
    while mutilated_area not in ('M', 'H'):
        mutilated_area = input('Invalid area. Choose \'M\' for mouth or ' + \
                               '\'H\' for hand: ')

    return mutilated, mutilated_area


def get_doctor_target(player_data):
    patient = input('Person to protect: ')
    while not _valid_target(patient, player_data):
        patient = input('Invalid target. Person to protect: ')

    return patient
