''' Implementation of the storyteller in the popular game 'Mafia' '''
import random
import math
import sys
import time

import mafia_api.email_api.gm_email as gm_email
import mafia_api.io_api.facade_io as io
import mafia_api.ui_api.ui as mafia_ui

from mafia_api.player_api.player import Player
import logger

suicidal_lynched = False

alive_cnt = []

player_data = {}

def assign_roles():
    ''' Randomly generates roles for each of the players. Also asks for number
    of players and names. '''
    roles_cnt = [0, 0, 0, 0, 0, 0, 0]
    roles_cnt[Player.PLAYER_IDX] = io.get_player_cnt()

    if roles_cnt[Player.PLAYER_IDX] < 5:
        io.output('Unfortunately, you cannot play with less than 5 people :(')
        return -1

    if roles_cnt[Player.PLAYER_IDX] > 20:
        io.output('Unfortunately, you cannot play with more than 20 people :(')
        return -1

    roles_cnt[Player.ASSN_IDX] = math.floor(1 + (roles_cnt[Player.PLAYER_IDX] - 5) / 4)
    roles_cnt[Player.POLICE_IDX] = math.floor(1 + (roles_cnt[Player.PLAYER_IDX] - 5) / 5)
    roles_cnt[Player.SUICD_IDX] = 1
    roles_cnt[Player.DOCTOR_IDX] = 1 + (roles_cnt[Player.PLAYER_IDX] >= 10)
    roles_cnt[Player.MTLT_IDX] = 1 + (roles_cnt[Player.PLAYER_IDX] >= 10)
    roles_cnt[Player.POTATO_IDX] = roles_cnt[Player.PLAYER_IDX] -\
                                      roles_cnt[Player.ASSN_IDX] -\
                                      roles_cnt[Player.POLICE_IDX] -\
                                      roles_cnt[Player.SUICD_IDX] -\
                                      roles_cnt[Player.DOCTOR_IDX] -\
                                      roles_cnt[Player.MTLT_IDX]

    global alive_cnt
    alive_cnt = roles_cnt

    role_list = []
    for i in range(roles_cnt[Player.ASSN_IDX]):
        role_list.append(Player.ASSN_IDX)

    for i in range(roles_cnt[Player.POLICE_IDX]):
        role_list.append(Player.POLICE_IDX)

    role_list.append(Player.SUICD_IDX)

    for i in range(roles_cnt[Player.DOCTOR_IDX]):
        role_list.append(Player.DOCTOR_IDX)

    for i in range(roles_cnt[Player.MTLT_IDX]):
        role_list.append(Player.MTLT_IDX)

    for i in range(roles_cnt[Player.POTATO_IDX]):
        role_list.append(Player.POTATO_IDX)

    random.shuffle(role_list)

    emails, msgs = io.get_names_emails(role_list,\
                                       roles_cnt[Player.PLAYER_IDX],\
                                       player_data)

    for i in range(roles_cnt[Player.PLAYER_IDX]):
        gm_email.send_email(emails[i], msgs[i])

    logger.log_info('\n')
    return 0


def kill(player_name):
    ''' Removes a player from the game, updating all the necessary structures.
    '''
    if player_name in player_data:
        player_data[player_name].die()
        alive_cnt[player_data[player_name].get_role_idx()] -= 1
        alive_cnt[Player.PLAYER_IDX] -= 1


def mafia_won():
    ''' True if mafia satisfies their win condition, False otherwise. '''
    return alive_cnt[Player.ASSN_IDX] >= alive_cnt[Player.PLAYER_IDX] -\
           alive_cnt[Player.ASSN_IDX]


def town_won():
    ''' True if town satisfies their win condition, False otherwise. '''
    return alive_cnt[Player.ASSN_IDX] == 0


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

    #logger.log_info('Still alive: '  + str(still_alive))
    io.add_logs('Still alive: '  + str(still_alive))

    lynched_name = io.get_lynched_name(can_vote, still_alive)

    if lynched_name != "NONE":
        while lynched_name not in player_data or not player_data[lynched_name].get_alive():
            lynched_name = input('Not a valid player.\nName of lynched player: ')

        if player_data[lynched_name].get_role_idx() == Player.SUICD_IDX:
            global suicidal_lynched
            suicidal_lynched = True

        kill(lynched_name)

    restore_voting_rights()
    #logger.log_info('\n---------- DAY ' + str(cycle_count) + ' END ----------\n')
    io.add_logs('\n---------- DAY ' + str(cycle_count) + ' END ----------\n')

def get_alive_players_minus_role(role_idx):
    ''' Get all live players except those that have a certain role. '''
    targets = []
    for name in player_data:
        if player_data[name].get_alive() and player_data[name].get_role_idx() != role_idx:
            targets.append(name)

    return targets


def get_assn_targets():
    ''' Returns a list of the names of valid assassination targets. '''
    return get_alive_players_minus_role(Player.ASSN_IDX)


def get_doctor_targets():
    ''' Returns a list of the names of valid doctor targets. '''
    return get_alive_players()


def get_mutilator_targets():
    ''' Returns a list of the names of valid mutilator targets. '''
    return get_alive_players()


def get_police_targets():
    ''' Returns a list of the names of valid police targets. '''
    return get_alive_players_minus_role(Player.POLICE_IDX)


def fake_night_action():
    ''' Waits for some time to fake that someone acted if said role
    no longer exists in game. '''
    if not logger.is_debug_mode():
        sleep_time = random.randint(6, 10)
        time.sleep(sleep_time)


def assn_night(assn_turn):
    ''' Simulates the assassins' night phase '''
    io.output('The assassins wake up.')
    if assn_turn:
        assassinated = io.get_assn_target(player_data, get_assn_targets())
    else:
        assassinated = None
        fake_night_action()

    io.output('The assassins go to sleep.\n')
    return assassinated


def police_night(police_turn):
    ''' Simulates the police's night phase '''
    io.output('The police wake up.')
    if police_turn:
        police_query = io.get_police_target(player_data, get_police_targets())
    else:
        police_query = None
        fake_night_action()

    # print('Query: ' + police_query)
    if police_query:
        io.show_police_answer(player_data, police_query)

    io.output('The police go to sleep.\n')


def mutilator_night(mutilator_turn):
    '''' Simulates the mutilators' night phase. '''
    io.output('The mutilators wake up.')
    if mutilator_turn:
        mtlt_targets = get_mutilator_targets()
        mutilated, mutilated_area = io.get_mutilator_target(player_data,\
                                                            mtlt_targets)

    else:
        mutilated = None
        mutilated_area = None
        fake_night_action()

    io.output('The mutilators go to sleep.\n')
    return mutilated, mutilated_area


def doctor_night(doctor_turn):
    ''' Simulates the doctors' night phase. '''
    io.output('The doctors wake up.')
    if doctor_turn:
        patient = io.get_doctor_target(player_data, get_doctor_targets())
    else:
        patient = None
        fake_night_action()

    io.output('The doctors go to sleep.\n')
    return patient


def pause_between_roles():
    ''' Introduces a pause between night actions so each player has time to get
    back to their seat. '''
    if not logger.is_debug_mode():
        time.sleep(4)


def play_night(cycle_count):
    ''' Simulates the next night phase in the game. '''

    # These symbolise if the respective turns can still act at night
    assn_turn = bool(alive_cnt[Player.ASSN_IDX])
    police_turn = bool(alive_cnt[Player.POLICE_IDX])
    doctor_turn = bool(alive_cnt[Player.DOCTOR_IDX])
    mutilator_turn = bool(alive_cnt[Player.MTLT_IDX])

    #logger.log_info('---------- NIGHT ' + str(cycle_count) + ' ----------\n')
    io.add_logs('---------- NIGHT ' + str(cycle_count) + ' ----------\n')
    io.output('Everyone goes to sleep.\n')

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

    #logger.log_info('---------- NIGHT ' + str(cycle_count) + ' END ----------\n')
    #logger.log_info('---------- DAY ' + str(cycle_count + 1) + ' ----------\n')
    io.add_logs('---------- NIGHT ' + str(cycle_count) + ' END ----------\n')
    io.add_logs('---------- DAY ' + str(cycle_count + 1) + ' ----------\n')


    io.output('Everyone wakes up.\n')
    if game_over():
        return

    if assassinated:
        io.output(assassinated + ' was assassinated.')
        kill(assassinated)
    else:
        io.output('Nobody was assassinated.')

    if mutilated and mutilated_area == 'M':
        io.output(mutilated + ' had his mouth mutilated. He cannot speak today.')
    elif mutilated:
        io.output(mutilated + ' had his hand mutilated. He cannot vote today.')
    else:
        io.output('Nobody was mutilated.')

    #logger.log_info('\n')
    io.add_logs("\n")


def play_game():
    ''' Runs the simulation. '''
    cycle_count = 1
    #logger.log_info('---------- DAY 1 ----------\n')
    io.add_logs('---------- DAY 1 ----------\n')

    while not game_over():
        play_day(cycle_count)
        if game_over():
            return

        play_night(cycle_count)
        cycle_count += 1


def log_results():
    ''' Prints the scoreboard. '''
    #logger.log_info('---------- RESULTS ----------')
    io.add_logs('---------- RESULTS ----------')
    if suicidal_won():
        io.output("The suicidal person won!\n")

    if mafia_won():
        io.output("The mafia won!\n")

    if town_won():
        io.output("The town won!\n")

    logger.log_info('\n')
    io.show_mafia(player_data)
    io.show_town(player_data)
    io.show_suicidal(player_data)


def start():
    ''' Starts a game of Mafia. '''
    mafia_ui.start_window_thread()
    if assign_roles():
        sys.exit()

    # Log all roles in debug mode
    for player_name in player_data:
        logger.log_debug(player_name + ' the ' + player_data[player_name].get_role_name() + '.')

    play_game()
    log_results()
