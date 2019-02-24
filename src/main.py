import random
import math
import sys
import os
import time
from argparse import ArgumentParser

PLAYER_IDX = 0
ASSN_IDX = 1
POLICE_IDX = 2
SUICD_IDX = 3
DOCTOR_IDX = 4
MTLT_IDX = 5
POTATO_IDX = 6

cycle_count = 1
debug_mode = None
speak_mode = None
suicidal_lynched = False

roles_cnt = [0, 0, 0, 0, 0, 0, 0]
alive_cnt = []

player_roles = {}
player_alive = {}

def output(text):
    if speak_mode:
        speak(text)
        print(text)
    else:
        print(text)


def speak(text):
    if sys.platform == 'darwin':
        os.system('say ' + text)


def assign_roles():
    # TODO: (Lulu) UI for entering names
    roles_cnt[PLAYER_IDX] = int(input('Enter number of players: '))
    if roles_cnt[PLAYER_IDX] < 5:
        output('Unfortunately, you can\'t play with less than 5 people :(')
        return -1;

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

    for i in range(roles_cnt[PLAYER_IDX]):
        curr_name = input('Enter player ' + str(i + 1) + ' name: ')
        while (curr_name == '' or curr_name in player_roles):
            curr_name = input('Please choose another name: ')

        rand_index = random.randint(0, len(role_list) - 1)
        player_roles[curr_name] = role_list.pop(rand_index);
        player_alive[curr_name] = True

    # print('\n')
    return 0
    # TODO: (Lulu) Make a UI so that everyone can find out their roles kthxbye


def kill(name):
    player_alive[name] = False
    alive_cnt[player_roles[name]] -= 1
    alive_cnt[PLAYER_IDX] -= 1


def role_idx_to_name(idx):
    if idx == 0:
        if debug_mode:
            print('DEBUG: Invalid role index')
        sys.exit()

    role_names = ['ERROR', 'assassin', 'policeman', 'suicidal person', 'doctor', 'mutilator', 'townie']
    return role_names[idx]


def mafia_won():
    return alive_cnt[ASSN_IDX] > alive_cnt[PLAYER_IDX] - alive_cnt[ASSN_IDX]


def town_won():
    return alive_cnt[ASSN_IDX] == 0


def suicidal_won():
    return suicidal_lynched


def game_over():
    return town_won() or mafia_won() or suicidal_won()


def play_day():
    # TODO: (Lulu) Make a UI for Lynching (lynched_name is name of victim)
    still_alive = []
    for name in player_alive:
        if player_alive[name]:
            still_alive.append(name)

    print('Still alive: '  + str(still_alive))

    lynched_name = input('Name of lynched player: ')
    if lynched_name != 'NONE':
        while lynched_name not in player_roles or player_alive[lynched_name] == False:
            lynched_name = input('Not a valid player.\nName of lynched player: ')

        if player_roles[lynched_name] == SUICD_IDX:
            global suicidal_lynched
            suicidal_lynched = True

        kill(lynched_name)

    print('\n---------- DAY ' + str(cycle_count) + ' END ----------\n')


def play_night():
    # These symbolise if the respective turns can still act at night
    assn_turn = bool(alive_cnt[ASSN_IDX])
    police_turn = bool(alive_cnt[POLICE_IDX])
    doctor_turn = bool(alive_cnt[DOCTOR_IDX])
    mutilator_turn = bool(alive_cnt[MTLT_IDX])

    # TODO: (Lulu) UI for every night action
    print('---------- NIGHT ' + str(cycle_count) + ' ----------\n')
    output('Everyone goes to sleep.\n')

    # Assn
    output('The assassins wake up.')
    if assn_turn:
        assassinated = input('Name of assassinee: ')
        while player_roles[assassinated] == ASSN_IDX:
            assassinated = input('You cannot kill fellow assassins. Name of assassinee: ')
    else:
        assassinated = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    output('The assassins go to sleep.\n')

    # Police
    output('The police wake up.')
    if police_turn:
        police_query = input('Person to query: ')
    else:
        police_query = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)
    
    if police_query and player_roles[police_query] == ASSN_IDX:
        print('The person you queried is an assassin.\n')
    elif police_query:
        print('The person you queried is NOT an assassin.\n')

    output('The police go to sleep.\n')

    # Mutilator
    output('The mutilators wake up.')
    if mutilator_turn:
        mutilated = input('Name of mutilatee: ')
        mutilated_area = input('Mutilated area (m/h): ')
    else:
        mutilated = None
        mutilated_area = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    output('The mutilators go to sleep.\n')

    # Doctor
    output('The doctors wake up.')
    if doctor_turn:
        patient = input('Name of patient: ')
    else:
        patient = None
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)

    if patient and patient == mutilated:
        mutilated = None

    if patient and patient == assassinated:
        assassinated = None

    output('The doctors go to sleep.\n')

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


def print_player(name):
    if player_alive[name]:
        status = 'ALIVE'
    else:
        status = 'DEAD'

    print(name + ' the ' + role_idx_to_name(player_roles[name]) + ' - ' + \
          status)


def print_mafia():
    print('Mafia:')
    for name in player_roles:
        if player_roles[name] != ASSN_IDX:
            continue

        print_player(name)

    print('\n')


def print_town():
    print('Town:')
    for name in player_roles:
        if player_roles[name] == ASSN_IDX or player_roles[name] == SUICD_IDX:
            continue

        print_player(name)

    print('\n')


def print_suicidal():
    print('Neutral:')
    for name in player_roles:
        if player_roles[name] == SUICD_IDX:
            print_player(name)
            break

    print('\n')


def print_results():
    # TODO: (Chris) print results
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
    print('---------- DAY 1 ----------\n')
    while not game_over():
        play_day()
        if game_over():
            return

        play_night()

        global cycle_count
        cycle_count += 1


# Execution starts here
parser = ArgumentParser()
parser.add_argument('-x', '--textonly', action = 'store_true',
                    help = 'Do not use voice commands')

parser.add_argument('-d', '--debug', action = 'store_true',
                    help = 'All input comes from console')

parser.add_argument('-t', '--test', action = 'store_true',
                    help = 'Run tests')

args = parser.parse_args()
debug_mode = args.debug
test_mode = args.test
speak_mode = not args.textonly

if assign_roles():
    sys.exit()

if debug_mode:
    # Print all the roles
    for name in player_roles:
        print(name + ' the ' + role_idx_to_name(player_roles[name]) + '.')

play_game()
print_results()
