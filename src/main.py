''' Implementation of the storyteller in the popular game 'Mafia' '''

import random
import math
import sys
import os
import time
import gm_email
import ui.ui as ui
import logger
import constants as ct
from argparse import ArgumentParser

suicidal_lynched = False

roles_cnt = [0, 0, 0, 0, 0, 0, 0]
alive_cnt = []

player_roles = {}
player_alive = {}

def assign_roles():
    ''' Randomly generates roles for each of the players. Also asks for number
    of players and names.
    '''

    roles_cnt[ct.PLAYER_IDX] = int(input('Enter number of players: '))
    if roles_cnt[ct.PLAYER_IDX] < 5:
        logger.output('Unfortunately, you cannot play with less than 5 people :(')
        return -1

    if roles_cnt[ct.PLAYER_IDX] > 20:
        logger.output('Unfortunately, you cannot play with more than 20 people :(')
        return -1

    roles_cnt[ct.ASSN_IDX] = math.floor(1 + (roles_cnt[ct.PLAYER_IDX] - 5) / 4)
    roles_cnt[ct.POLICE_IDX] = math.floor(1 + (roles_cnt[ct.PLAYER_IDX] - 5) / 5)
    roles_cnt[ct.SUICD_IDX] = 1
    roles_cnt[ct.DOCTOR_IDX] = 1 + (roles_cnt[ct.PLAYER_IDX] >= 10)
    roles_cnt[ct.MTLT_IDX] = 1 + (roles_cnt[ct.PLAYER_IDX] >= 10)
    roles_cnt[ct.POTATO_IDX] = roles_cnt[ct.PLAYER_IDX] - roles_cnt[ct.ASSN_IDX] - \
                            roles_cnt[ct.POLICE_IDX] - roles_cnt[ct.SUICD_IDX] - \
                            roles_cnt[ct.DOCTOR_IDX] - roles_cnt[ct.MTLT_IDX]

    global alive_cnt
    alive_cnt = roles_cnt

    role_list = []
    for i in range(roles_cnt[ct.ASSN_IDX]):
        role_list.append(ct.ASSN_IDX)

    for i in range(roles_cnt[ct.POLICE_IDX]):
        role_list.append(ct.POLICE_IDX)

    role_list.append(ct.SUICD_IDX)

    for i in range(roles_cnt[ct.DOCTOR_IDX]):
        role_list.append(ct.DOCTOR_IDX)

    for i in range(roles_cnt[ct.MTLT_IDX]):
        role_list.append(ct.MTLT_IDX)

    for i in range(roles_cnt[ct.POTATO_IDX]):
        role_list.append(ct.POTATO_IDX)

    random.shuffle(role_list)

    emails = []
    msgs = []
    for i in range(roles_cnt[ct.PLAYER_IDX]):
        curr_name = input('Enter player ' + str(i + 1) + ' name: ')
        while (curr_name == '' or curr_name in player_roles):
            curr_name = input('Please choose another name: ')

        curr_email = input('Enter player ' + str(i + 1) + ' e-mail: ')
        # sure = input('Are you sure (y for yes)?')
        # while sure != 'y':
        #     curr_email = input('Enter player ' + str(i + 1) + ' e-mail: ')
        #     sure = input('Are you sure (y for yes)?')

        rand_index = random.randint(0, len(role_list) - 1)
        player_roles[curr_name] = role_list.pop(rand_index)
        player_alive[curr_name] = True

        curr_msg = 'Hi ' + curr_name + '! Your role for this round is ' + \
                   logger.role_idx_to_name(player_roles[curr_name]) + '.'

        emails.append(curr_email)
        msgs.append(curr_msg)

    for i in range(roles_cnt[ct.PLAYER_IDX]):
        gm_email.send_email(emails[i], msgs[i])

    logger.log_info('\n')
    return 0


def kill(player_name):
    ''' Removes a player from the game, updating all the necessary structures.
    '''
    player_alive[player_name] = False
    alive_cnt[player_roles[player_name]] -= 1
    alive_cnt[ct.PLAYER_IDX] -= 1


def mafia_won():
    ''' True if mafia satisfies their win condition, False otherwise. '''
    return alive_cnt[ct.ASSN_IDX] >= alive_cnt[ct.PLAYER_IDX] - alive_cnt[ct.ASSN_IDX]


def town_won():
    ''' True if town satisfies their win condition, False otherwise. '''
    return alive_cnt[ct.ASSN_IDX] == 0


def suicidal_won():
    ''' True if the suicidal person satisfies their win condition, False
    otherwise.
    '''
    return suicidal_lynched


def game_over():
    ''' True if any of the factions satisfy their win condition.
    '''
    return town_won() or mafia_won() or suicidal_won()


def get_alive_players():
    ''' Returns a list of all players that are still alive. '''
    targets = []
    for name in player_roles:
        if player_alive[name]:
            targets.append(name)

    return targets


def play_day(cycle_count):
    ''' Simulates the next daytime phase in the game. '''

    still_alive = get_alive_players()
    logger.log_info('Still alive: '  + str(still_alive))

    if logger.is_debug_mode():
        lynched_name = input('Name of lynched player: ')
    else:
        lynched_name = ui.day_vote(still_alive)

    if lynched_name != 'NONE':
        while lynched_name not in player_roles or not player_alive[lynched_name]:
            lynched_name = input('Not a valid player.\nName of lynched player: ')

        if player_roles[lynched_name] == ct.SUICD_IDX:
            global suicidal_lynched
            suicidal_lynched = True

        kill(lynched_name)

    logger.log_info('\n---------- DAY ' + str(cycle_count) + ' END ----------\n')


def valid_target(player_name):
    ''' Checks if a player is in the game and alive. '''
    return player_name in player_roles and player_alive[player_name]


def get_alive_players_minus_role(role_idx):
    targets = []
    for name in player_roles:
        if player_alive[name] and player_roles[name] != role_idx:
            targets.append(name)

    return targets


def get_assn_targets():
    ''' Returns a list of the names of valid assassination targets. '''
    return get_alive_players_minus_role(ct.ASSN_IDX)


def get_doctor_targets():
    ''' Returns a list of the names of valid doctor targets. '''
    return get_alive_players()


def get_mutilator_targets():
    ''' Returns a list of the names of valid mutilator targets. '''
    return get_alive_players()


def get_police_targets():
    ''' Returns a list of the names of valid police targets. '''
    return get_alive_players_minus_role(ct.POLICE_IDX)


def assn_night(assn_turn):
    ''' Simulates the assassins' night phase '''
    logger.output('The assassins wake up.')
    if assn_turn and logger.is_debug_mode():
        assassinated = input('Person to assassinate: ')
        while not valid_target(assassinated) or\
              player_roles[assassinated] == ct.ASSN_IDX:

            assassinated = input('Invalid target. Person to assassinate: ')
    elif assn_turn and not logger.is_debug_mode():
        assassinated = ui.night_assassin_vote(get_assn_targets())
    else:
        assassinated = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    logger.output('The assassins go to sleep.\n')
    return assassinated


def police_night(police_turn):
    ''' Simulates the police's night phase '''
    logger.output('The police wake up.')
    if police_turn and logger.is_debug_mode():
        police_query = input('Person to query: ')
        while not valid_target(police_query):
            police_query = input('Invalid target. Person to query: ')
    elif police_turn and not logger.is_debug_mode():
        police_query = ui.night_cop_vote(get_police_targets())
    else:
        police_query = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)
    if logger.is_debug_mode():
        if police_query and player_roles[police_query] == ct.ASSN_IDX:
            logger.log_info('The person you queried is an assassin.\n')
        elif police_query:
            logger.log_info('The person you queried is NOT an assassin.\n')
    elif not logger.is_debug_mode():
        if police_query and player_roles[police_query] == ct.ASSN_IDX:
            ui.show_info('The person you queried is an assassin.\n')
        elif police_query:
            ui.show_info('The person you queried is NOT an assassin.\n')


    logger.output('The police go to sleep.\n')


def mutilator_night(mutilator_turn):
    '''' Simulates the mutilators' night phase. '''
    logger.output('The mutilators wake up.')
    if mutilator_turn and logger.is_debug_mode():
        mutilated = input('Person to mutilate: ')
        while not valid_target(mutilated):
            mutilated = input('Invalid target. Person to mutilate: ')

        mutilated_area = input('Area to mutilate (M/H): ')
        while mutilated_area not in ('M', 'H'):
            mutilated_area = input('Invalid area. Choose \'m\' for mouth or ' + \
                                   '\'h\' for hand: ')
    elif mutilator_turn and not logger.is_debug_mode():
        mutilated, mutilated_area = ui.night_mutilator_vote(get_mutilator_targets())
    else:
        mutilated = None
        mutilated_area = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    logger.output('The mutilators go to sleep.\n')
    return mutilated, mutilated_area


def doctor_night(doctor_turn):
    ''' Simulates the doctors' night phase. '''
    logger.output('The doctors wake up.')
    if doctor_turn and logger.is_debug_mode():
        patient = input('Person to protect: ')
        while not valid_target(patient):
            patient = input('Invalid target. Person to protect: ')
    elif doctor_turn and not logger.is_debug_mode():
        patient = ui.night_doctor_vote(get_doctor_targets())
    else:
        patient = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    logger.output('The doctors go to sleep.\n')
    return patient


def play_night(cycle_count):
    ''' Simulates the next night phase in the game. '''

    # These symbolise if the respective turns can still act at night
    assn_turn = bool(alive_cnt[ct.ASSN_IDX])
    police_turn = bool(alive_cnt[ct.POLICE_IDX])
    doctor_turn = bool(alive_cnt[ct.DOCTOR_IDX])
    mutilator_turn = bool(alive_cnt[ct.MTLT_IDX])

    logger.log_info('---------- NIGHT ' + str(cycle_count) + ' ----------\n')
    logger.output('Everyone goes to sleep.\n')

    assassinated = assn_night(assn_turn)
    police_night(police_turn)
    mutilated, mutilated_area = mutilator_night(mutilator_turn)
    patient = doctor_night(doctor_turn)

    if patient and patient == mutilated:
        mutilated = None

    if patient and patient == assassinated:
        assassinated = None

    logger.log_info('---------- NIGHT ' + str(cycle_count) + ' END ----------\n')
    logger.log_info('---------- DAY ' + str(cycle_count + 1) + ' ----------\n')

    logger.output('Everyone wakes up.\n')
    if game_over():
        return

    if assassinated:
        logger.output(assassinated + ' was assassinated.')
        kill(assassinated)
    else:
        logger.output('Nobody was assassinated.')

    if mutilated and mutilated_area == 'M':
        logger.output(mutilated + ' had his mouth mutilated. He cannot speak today.')
    elif mutilated:
        logger.output(mutilated + ' had his hand mutilated. He cannot vote today.')
    else:
        logger.output('Nobody was mutilated.')

    logger.log_info('\n')


def play_game():
    ''' Runs the simulation. '''
    cycle_count = 1
    logger.log_info('---------- DAY 1 ----------\n')
    while not game_over():
        play_day(cycle_count)
        if game_over():
            return

        play_night(cycle_count)
        cycle_count += 1


def log_results():
    ''' Prints the scoreboard. '''
    logger.log_info('---------- RESULTS ----------')
    if suicidal_won():
        logger.output("The suicidal person won!\n")

    if mafia_won():
        logger.output("The mafia won!\n")

    if town_won():
        logger.output("The town won!\n")

    logger.log_info('\n')
    logger.log_mafia(player_roles, player_alive)
    logger.log_town(player_roles, player_alive)
    logger.log_suicidal(player_roles, player_alive)


# Execution starts here
parser = ArgumentParser()
parser.add_argument('-x', '--textonly', action='store_true',
                    help='Do not use voice commands')

parser.add_argument('-d', '--debug', action='store_true',
                    help='All input comes from console')

args = parser.parse_args()
logger.set_debug_mode(args.debug)
logger.set_speak_mode(not args.textonly)

if assign_roles():
    sys.exit()

logger.dbg_log_all_roles(player_roles)

play_game()
log_results()
# TODO: (Chris) implement hand mutilation logic (day voting)
# TODO: (Chris) Switch to the email UI
# TODO: (Chris) Make the breaks between roles during the night bigger so people have time(for real games)
