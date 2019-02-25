''' Implementation of the storyteller in the popular game 'Mafia' '''

import random
import math
import sys
import os
import time
import gm_email
from argparse import ArgumentParser

PLAYER_IDX = 0
ASSN_IDX = 1
POLICE_IDX = 2
SUICD_IDX = 3
DOCTOR_IDX = 4
MTLT_IDX = 5
POTATO_IDX = 6

DEBUG_MODE = None
SPEAK_MODE = None
suicidal_lynched = False

roles_cnt = [0, 0, 0, 0, 0, 0, 0]
alive_cnt = []

player_roles = {}
player_alive = {}

def output(text):
    ''' Speaks and prints the input text if SPEAK_MODE is enabled. Prints
    otherwise
    '''
    if SPEAK_MODE:
        speak(text)
        print(text)
    else:
        print(text)


def speak(text):
    ''' Wrapper for platform specific text-to-speech functionality. Should be
    called similar to print().
    '''
    # TODO: (Chris) add text-to-speech for Windows and Linux
    if sys.platform == 'darwin':
        os.system('say ' + '"' + text + '"')


def assign_roles():
    ''' Randomly generates roles for each of the players. Also asks for number
    of players and names.
    '''

    # TODO: (Lulu) UI for entering names
    roles_cnt[PLAYER_IDX] = int(input('Enter number of players: '))
    # if roles_cnt[PLAYER_IDX] < 5:
        # output('Unfortunately, you cannot play with less than 5 people :(')
        # return -1

    if roles_cnt[PLAYER_IDX] > 20:
        output('Unfortunately, you cannot play with more than 20 people :(')
        return -1

    roles_cnt[ASSN_IDX] = math.floor(1 + (roles_cnt[PLAYER_IDX] - 5) / 4)
    roles_cnt[POLICE_IDX] = math.floor(1 + (roles_cnt[PLAYER_IDX] - 5) / 5)
    roles_cnt[SUICD_IDX] = 1
    roles_cnt[DOCTOR_IDX] = 1 + (roles_cnt[PLAYER_IDX] >= 10)
    roles_cnt[MTLT_IDX] = 1 + (roles_cnt[PLAYER_IDX] >= 10)
    roles_cnt[POTATO_IDX] = roles_cnt[PLAYER_IDX] - roles_cnt[ASSN_IDX] - \
                            roles_cnt[POLICE_IDX] - roles_cnt[SUICD_IDX] - \
                            roles_cnt[DOCTOR_IDX] - roles_cnt[MTLT_IDX]

    global alive_cnt
    alive_cnt = roles_cnt

    role_list = []
    for i in range(roles_cnt[ASSN_IDX]):
        role_list.append(ASSN_IDX)

    for i in range(roles_cnt[POLICE_IDX]):
        role_list.append(POLICE_IDX)

    role_list.append(SUICD_IDX)

    for i in range(roles_cnt[DOCTOR_IDX]):
        role_list.append(DOCTOR_IDX)

    for i in range(roles_cnt[MTLT_IDX]):
        role_list.append(MTLT_IDX)

    for i in range(roles_cnt[POTATO_IDX]):
        role_list.append(POTATO_IDX)

    random.shuffle(role_list)

    emails = []
    msgs = []
    for i in range(roles_cnt[PLAYER_IDX]):
        curr_name = input('Enter player ' + str(i + 1) + ' name: ')
        while (curr_name == '' or curr_name in player_roles):
            curr_name = input('Please choose another name: ')

        curr_email = input('Enter player ' + str(i + 1) + ' e-mail: ')
        sure = input('Are you sure (y for yes)?')
        while sure != 'y':
            curr_email = input('Enter player ' + str(i + 1) + ' e-mail: ')
            sure = input('Are you sure (y for yes)?')

        rand_index = random.randint(0, len(role_list) - 1)
        player_roles[curr_name] = role_list.pop(rand_index)
        player_alive[curr_name] = True

        curr_msg = 'Hi ' + curr_name + '! Your role for this round is ' + \
                   role_idx_to_name(player_roles[curr_name]) + '.'

        emails.append(curr_email)
        msgs.append(curr_msg)

    for i in range(roles_cnt[PLAYER_IDX]):
        gm_email.send_email(emails[i], msgs[i])

    print('\n')
    return 0
    # TODO: (Lulu) Make a UI so that everyone can find out their roles kthxbye


def kill(player_name):
    ''' Removes a player from the game, updating all the necessary structures.
    '''

    player_alive[player_name] = False
    alive_cnt[player_roles[player_name]] -= 1
    alive_cnt[PLAYER_IDX] -= 1


def role_idx_to_name(idx):
    ''' Converts a role index constant to the actual role name.'''

    if idx == 0:
        if DEBUG_MODE:
            print('DEBUG: Invalid role index')
        sys.exit()

    role_names = ['ERROR', 'assassin', 'policeman', 'suicidal person',\
                  'doctor', 'mutilator', 'townie']
    return role_names[idx]


def mafia_won():
    ''' True if mafia satisfies their win condition, False otherwise. '''
    return alive_cnt[ASSN_IDX] >= alive_cnt[PLAYER_IDX] - alive_cnt[ASSN_IDX]


def town_won():
    ''' True if town satisfies their win condition, False otherwise. '''
    return alive_cnt[ASSN_IDX] == 0


def suicidal_won():
    ''' True if the suicidal person satisfies their win condition, False
    otherwise.
    '''
    return suicidal_lynched


def game_over():
    ''' True if any of the factions satisfy their win condition.
    '''
    return town_won() or mafia_won() or suicidal_won()


def play_day(cycle_count):
    ''' Simulates the next daytime phase in the game. '''

    # TODO: (Lulu) Make a UI for Lynching (lynched_name is name of victim)
    still_alive = []
    for player_name in player_alive:
        if player_alive[player_name]:
            still_alive.append(player_name)

    print('Still alive: '  + str(still_alive))

    lynched_name = input('Name of lynched player: ')
    if lynched_name != 'NONE':
        while lynched_name not in player_roles or not player_alive[lynched_name]:
            lynched_name = input('Not a valid player.\nName of lynched player: ')

        if player_roles[lynched_name] == SUICD_IDX:
            global suicidal_lynched
            suicidal_lynched = True

        kill(lynched_name)

    print('\n---------- DAY ' + str(cycle_count) + ' END ----------\n')


def valid_target(player_name):
    ''' Checks if a player is in the game and alive. '''
    return player_name in player_roles and player_alive[player_name]


def assn_night(assn_turn):
    ''' Simulates the assassins' night phase '''
    output('The assassins wake up.')
    if assn_turn:
        assassinated = input('Person to assassinate: ')
        while not valid_target(assassinated) or\
              player_roles[assassinated] == ASSN_IDX:

            assassinated = input('Invalid target. Person to assassinate: ')
    else:
        assassinated = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    output('The assassins go to sleep.\n')
    return assassinated


def police_night(police_turn):
    ''' Simulates the police's night phase '''
    output('The police wake up.')
    if police_turn:
        police_query = input('Person to query: ')
        while not valid_target(police_query):
            police_query = input('Invalid target. Person to query: ')
    else:
        police_query = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    if police_query and player_roles[police_query] == ASSN_IDX:
        print('The person you queried is an assassin.\n')
    elif police_query:
        print('The person you queried is NOT an assassin.\n')

    output('The police go to sleep.\n')


def mutilator_night(mutilator_turn):
    '''' Simulates the mutilators' night phase. '''
    output('The mutilators wake up.')
    if mutilator_turn:
        mutilated = input('Person to mutilate: ')
        while not valid_target(mutilated):
            mutilated = input('Invalid target. Person to mutilate: ')

        mutilated_area = input('Area to mutilate (m/h): ')
        while mutilated_area not in ('m', 'h'):
            mutilated_area = input('Invalid area. Choose \'m\' for mouth or ' + \
                                   '\'h\' for hand: ')
    else:
        mutilated = None
        mutilated_area = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    output('The mutilators go to sleep.\n')
    return mutilated, mutilated_area


def doctor_night(doctor_turn):
    ''' Simulates the doctors' night phase. '''
    output('The doctors wake up.')
    if doctor_turn:
        patient = input('Person to protect: ')
        while not valid_target(patient):
            patient = input('Invalid target. Person to protect: ')
    else:
        patient = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    output('The doctors go to sleep.\n')
    return patient


def play_night(cycle_count):
    ''' Simulates the next night phase in the game. '''

    # These symbolise if the respective turns can still act at night
    assn_turn = bool(alive_cnt[ASSN_IDX])
    police_turn = bool(alive_cnt[POLICE_IDX])
    doctor_turn = bool(alive_cnt[DOCTOR_IDX])
    mutilator_turn = bool(alive_cnt[MTLT_IDX])

    # TODO: (Lulu) UI for every night action
    print('---------- NIGHT ' + str(cycle_count) + ' ----------\n')
    output('Everyone goes to sleep.\n')

    assassinated = assn_night(assn_turn)
    police_night(police_turn)
    mutilated, mutilated_area = mutilator_night(mutilator_turn)
    patient = doctor_night(doctor_turn)

    if patient and patient == mutilated:
        mutilated = None

    if patient and patient == assassinated:
        assassinated = None

    print('---------- NIGHT ' + str(cycle_count) + ' END ----------\n')
    print('---------- DAY ' + str(cycle_count + 1) + ' ----------\n')

    output('Everyone wakes up.\n')
    if game_over():
        return

    if assassinated:
        output(assassinated + ' was assassinated.')
        kill(assassinated)
    else:
        output('Nobody was assassinated.')

    if mutilated and mutilated_area == 'm':
        output(mutilated + ' had his mouth mutilated. He cannot speak today.')
    elif mutilated:
        output(mutilated + ' had his hand mutilated. He cannot vote today.')
    else:
        output('Nobody was mutilated.')

    print('\n')


def print_player(player_name):
    ''' Prints the role and status (dead/alive) of a player. '''
    if player_alive[player_name]:
        status = 'ALIVE'
    else:
        status = 'DEAD'

    print(player_name + ' the ' + role_idx_to_name(player_roles[player_name]) + ' - ' + \
          status)


def print_mafia():
    ''' Prints all members of the mafia. '''
    print('Mafia:')
    for player_name in player_roles:
        if player_roles[player_name] != ASSN_IDX:
            continue

        print_player(player_name)

    print('\n')


def print_town():
    ''' Prints all members of the town. '''
    print('Town:')
    for player_name in player_roles:
        if player_roles[player_name] == ASSN_IDX or player_roles[player_name] == SUICD_IDX:
            continue

        print_player(player_name)

    print('\n')


def print_suicidal():
    ''' Prints the suicidal person. '''
    print('Neutral:')
    for player_name in player_roles:
        if player_roles[player_name] == SUICD_IDX:
            print_player(player_name)
            break

    print('\n')


def print_results():
    ''' Prints the scoreboard. '''
    print('---------- RESULTS ----------')
    if suicidal_won():
        output("The suicidal person won!\n")

    if mafia_won():
        output("The mafia won!\n")

    if town_won():
        output("The town won!\n")

    print('\n')
    print_mafia()
    print_town()
    print_suicidal()


def play_game():
    ''' Runs the simulation. '''
    cycle_count = 1
    print('---------- DAY 1 ----------\n')
    while not game_over():
        play_day(cycle_count)
        if game_over():
            return

        play_night(cycle_count)
        cycle_count += 1


# Execution starts here
parser = ArgumentParser()
parser.add_argument('-x', '--textonly', action='store_true',
                    help='Do not use voice commands')

parser.add_argument('-d', '--debug', action='store_true',
                    help='All input comes from console')

parser.add_argument('-t', '--test', action='store_true', help='Run tests')

args = parser.parse_args()
DEBUG_MODE = args.debug
TEST_MODE = args.test
SPEAK_MODE = not args.textonly

if assign_roles():
    sys.exit()

if DEBUG_MODE:
    # Print all the roles
    for dbg_name in player_roles:
        print(dbg_name + ' the ' + role_idx_to_name(player_roles[dbg_name]) + '.')

play_game()
print_results()
