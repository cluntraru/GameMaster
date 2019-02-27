''' Implementation of the storyteller in the popular game 'Mafia' '''

import random
import math
import sys
import time
from argparse import ArgumentParser

import gm_email
import ui
import logger
import player as pl

suicidal_lynched = False

alive_cnt = []

player_data = {}

def get_msg_from_name(name):
    ''' Returns message to email to player containing role. '''
    return 'Hi ' + name + '! Your role for this round is ' +\
           player_data[name].get_role_name() + '.'


def assign_roles():
    ''' Randomly generates roles for each of the players. Also asks for number
    of players and names.
    '''
    roles_cnt = [0, 0, 0, 0, 0, 0, 0]

    if logger.is_debug_mode():
        roles_cnt[pl.Player.PLAYER_IDX] = int(input('Enter number of players: '))
    else:
        roles_cnt[pl.Player.PLAYER_IDX] = ui.get_players_number()

    if roles_cnt[pl.Player.PLAYER_IDX] < 5:
        logger.output('Unfortunately, you cannot play with less than 5 people :(')
        return -1

    if roles_cnt[pl.Player.PLAYER_IDX] > 20:
        logger.output('Unfortunately, you cannot play with more than 20 people :(')
        return -1

    roles_cnt[pl.Player.ASSN_IDX] = math.floor(1 + (roles_cnt[pl.Player.PLAYER_IDX] - 5) / 4)
    roles_cnt[pl.Player.POLICE_IDX] = math.floor(1 + (roles_cnt[pl.Player.PLAYER_IDX] - 5) / 5)
    roles_cnt[pl.Player.SUICD_IDX] = 1
    roles_cnt[pl.Player.DOCTOR_IDX] = 1 + (roles_cnt[pl.Player.PLAYER_IDX] >= 10)
    roles_cnt[pl.Player.MTLT_IDX] = 1 + (roles_cnt[pl.Player.PLAYER_IDX] >= 10)
    roles_cnt[pl.Player.POTATO_IDX] = roles_cnt[pl.Player.PLAYER_IDX] - roles_cnt[pl.Player.ASSN_IDX] - \
                            roles_cnt[pl.Player.POLICE_IDX] - roles_cnt[pl.Player.SUICD_IDX] - \
                            roles_cnt[pl.Player.DOCTOR_IDX] - roles_cnt[pl.Player.MTLT_IDX]

    global alive_cnt
    alive_cnt = roles_cnt

    role_list = []
    for i in range(roles_cnt[pl.Player.ASSN_IDX]):
        role_list.append(pl.Player.ASSN_IDX)

    for i in range(roles_cnt[pl.Player.POLICE_IDX]):
        role_list.append(pl.Player.POLICE_IDX)

    role_list.append(pl.Player.SUICD_IDX)

    for i in range(roles_cnt[pl.Player.DOCTOR_IDX]):
        role_list.append(pl.Player.DOCTOR_IDX)

    for i in range(roles_cnt[pl.Player.MTLT_IDX]):
        role_list.append(pl.Player.MTLT_IDX)

    for i in range(roles_cnt[pl.Player.POTATO_IDX]):
        role_list.append(pl.Player.POTATO_IDX)

    random.shuffle(role_list)

    emails = []
    msgs = []
    if logger.is_debug_mode():
        for i in range(roles_cnt[pl.Player.PLAYER_IDX]):
            curr_name = input('Enter player ' + str(i + 1) + ' name: ')
            while (curr_name == '' or curr_name in player_data):
                curr_name = input('Please choose another name: ')

            curr_email = input('Enter player ' + str(i + 1) + ' e-mail: ')

            rand_index = random.randint(0, len(role_list) - 1)
            player_data[curr_name] = pl.Player(role_list.pop(rand_index))

            curr_msg = get_msg_from_name(curr_name)

            emails.append(curr_email)
            msgs.append(curr_msg)
    else:
        names_emails = ui.get_emails_form(roles_cnt[pl.Player.PLAYER_IDX])
        for name_email in names_emails:
            curr_name, curr_email = name_email

            rand_index = random.randint(0, len(role_list) - 1)
            player_data[curr_name] = pl.Player(role_list.pop(rand_index))

            curr_msg = get_msg_from_name(curr_name)

            emails.append(curr_email)
            msgs.append(curr_msg)

    for i in range(roles_cnt[pl.Player.PLAYER_IDX]):
        gm_email.send_email(emails[i], msgs[i])

    logger.log_info('\n')
    return 0


def kill(player_name):
    ''' Removes a player from the game, updating all the necessary structures.
    '''
    player_data[player_name].die()
    alive_cnt[player_data[player_name].get_role_idx()] -= 1
    alive_cnt[pl.Player.PLAYER_IDX] -= 1


def mafia_won():
    ''' True if mafia satisfies their win condition, False otherwise. '''
    return alive_cnt[pl.Player.ASSN_IDX] >= alive_cnt[pl.Player.PLAYER_IDX] - alive_cnt[pl.Player.ASSN_IDX]


def town_won():
    ''' True if town satisfies their win condition, False otherwise. '''
    return alive_cnt[pl.Player.ASSN_IDX] == 0


def suicidal_won():
    ''' True if the suicidal person satisfies their win condition, False
    otherwise. '''
    return suicidal_lynched


def game_over():
    ''' True if any of the factions satisfy their win condition. '''
    return town_won() or mafia_won() or suicidal_won()


def get_alive_players():
    ''' Returns a list of all players that are still alive. '''
    targets = []
    for name in player_data:
        if player_data[name].get_alive():
            targets.append(name)

    return targets


def get_voting_players():
    ''' Returns a list of players that are able to vote. '''
    targets = []
    for name in player_data:
        if player_data[name].get_alive() and player_data[name].get_can_vote():
            targets.append(name)

    return targets


def restore_voting_rights():
    ''' Restore voting rights to all players. '''
    for name in player_data:
        player_data[name].set_can_vote(True)


def play_day(cycle_count):
    ''' Simulates the next daytime phase in the game. '''
    still_alive = get_alive_players()
    can_vote = get_voting_players()

    logger.log_info('Still alive: '  + str(still_alive))

    if logger.is_debug_mode():
        lynched_name = input('Name of lynched player: ')
    else:
        lynched_name = ui.day_vote(can_vote, still_alive)

    if lynched_name != 'NONE':
        while lynched_name not in player_data or not player_data[lynched_name].get_alive():
            lynched_name = input('Not a valid player.\nName of lynched player: ')

        if player_data[lynched_name].get_role_idx() == pl.Player.SUICD_IDX:
            global suicidal_lynched
            suicidal_lynched = True

        kill(lynched_name)

    restore_voting_rights()
    logger.log_info('\n---------- DAY ' + str(cycle_count) + ' END ----------\n')


def valid_target(player_name):
    ''' Checks if a player is in the game and alive. '''
    return player_name in player_data and player_data[player_name].get_alive()


def get_alive_players_minus_role(role_idx):
    ''' Get all live players except those that have a certain role. '''
    targets = []
    for name in player_data:
        if player_data[name].get_alive() and player_data[name].get_role_idx() != role_idx:
            targets.append(name)

    return targets


def get_assn_targets():
    ''' Returns a list of the names of valid assassination targets. '''
    return get_alive_players_minus_role(pl.Player.ASSN_IDX)


def get_doctor_targets():
    ''' Returns a list of the names of valid doctor targets. '''
    return get_alive_players()


def get_mutilator_targets():
    ''' Returns a list of the names of valid mutilator targets. '''
    return get_alive_players()


def get_police_targets():
    ''' Returns a list of the names of valid police targets. '''
    return get_alive_players_minus_role(pl.Player.POLICE_IDX)


def fake_night_action():
    ''' Waits for some time to fake that someone acted if said role
    no longer exists in game. '''
    if not logger.is_debug_mode():
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)


def assn_night(assn_turn):
    ''' Simulates the assassins' night phase '''
    logger.output('The assassins wake up.')
    if assn_turn and logger.is_debug_mode():
        assassinated = input('Person to assassinate: ')
        while not valid_target(assassinated) or\
              player_data[assassinated].get_role_idx() == pl.Player.ASSN_IDX:

            assassinated = input('Invalid target. Person to assassinate: ')
    elif assn_turn and not logger.is_debug_mode():
        assassinated = ui.night_assassin_vote(get_assn_targets())
    else:
        assassinated = None
        fake_night_action()

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
        fake_night_action()

    if logger.is_debug_mode():
        if police_query and player_data[police_query].get_role_idx() == pl.Player.ASSN_IDX:
            logger.log_info('The person you queried is an assassin.\n')
        elif police_query:
            logger.log_info('The person you queried is NOT an assassin.\n')
    elif not logger.is_debug_mode():
        if police_query and player_data[police_query].get_role_idx() == pl.Player.ASSN_IDX:
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
            mutilated_area = input('Invalid area. Choose \'M\' for mouth or ' + \
                                   '\'H\' for hand: ')
    elif mutilator_turn and not logger.is_debug_mode():
        mutilated, mutilated_area = ui.night_mutilator_vote(get_mutilator_targets())
    else:
        mutilated = None
        mutilated_area = None
        fake_night_action()

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
        fake_night_action()

    logger.output('The doctors go to sleep.\n')
    return patient


def pause_between_roles():
    ''' Introduces a pause between night actions so each player has time to get
    back to their seat. '''
    if not logger.is_debug_mode():
        time.sleep(4)


def play_night(cycle_count):
    ''' Simulates the next night phase in the game. '''

    # These symbolise if the respective turns can still act at night
    assn_turn = bool(alive_cnt[pl.Player.ASSN_IDX])
    police_turn = bool(alive_cnt[pl.Player.POLICE_IDX])
    doctor_turn = bool(alive_cnt[pl.Player.DOCTOR_IDX])
    mutilator_turn = bool(alive_cnt[pl.Player.MTLT_IDX])

    logger.log_info('---------- NIGHT ' + str(cycle_count) + ' ----------\n')
    logger.output('Everyone goes to sleep.\n')

    pause_between_roles()
    assassinated = assn_night(assn_turn)
    pause_between_roles()

    police_night(police_turn)
    pause_between_roles()

    mutilated, mutilated_area = mutilator_night(mutilator_turn)
    pause_between_roles()

    patient = doctor_night(doctor_turn)
    pause_between_roles()

    if patient and patient == mutilated:
        mutilated = None
    elif not patient and mutilated and mutilated_area == 'H':
        player_data[mutilated].set_can_vote(False)

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
    logger.log_mafia(player_data)
    logger.log_town(player_data)
    logger.log_suicidal(player_data)


# Execution starts here
parser = ArgumentParser()
parser.add_argument('-x', '--textonly', action='store_true',
                    help='Do not use voice output')

parser.add_argument('-d', '--debug', action='store_true',
                    help='All input comes from console')

args = parser.parse_args()
logger.set_debug_mode(args.debug)
logger.set_speak_mode(not args.textonly)

if assign_roles():
    sys.exit()

logger.dbg_log_all_roles(player_data)

play_game()
log_results()
