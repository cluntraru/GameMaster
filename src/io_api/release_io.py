''' Functions that get input from UI. '''
import random
import player_api.player as pl
import ui_api.ui as ui
import email_api.gm_email as email

def get_player_cnt():
    ''' UI prompts for number of players and returns the result. '''
    return ui.get_players_number()


def get_names_emails(role_list, player_cnt, player_data):
    ''' UI prompts for player names and emails and returns a pair of arrays.
    '''
    emails = []
    msgs = []
    names_emails = ui.get_emails_form(player_cnt)
    for name_email in names_emails:
        curr_name, curr_email = name_email

        rand_index = random.randint(0, len(role_list) - 1)
        player_data[curr_name] = pl.Player(role_list.pop(rand_index))

        curr_msg = email.get_msg_from_name(curr_name, player_data)

        emails.append(curr_email)
        msgs.append(curr_msg)

    return emails, msgs


def get_lynched_name(can_vote, still_alive):
    ''' Starts day voting UI prompts and returns the result. '''
    return ui.day_vote(can_vote, still_alive)


def get_assn_target(targets):
    ''' UI prompts for assassination target and returns the result. '''
    return ui.night_assassin_vote(targets)


def get_police_target(targets):
    ''' UI prompts for police interrogation and returns the chosen person's
    name. '''
    return ui.night_cop_vote(targets)


def show_police_answer(player_data, target):
    ''' UI alerts whether the person interrogated by the police is an assassin or
    not. '''
    if target != "NONE":
        if player_data[target].is_assn():
            ui.show_info('The person you queried is an assassin.\n')
        else:
            ui.show_info('The person you queried is NOT an assassin.\n')


def get_mutilator_target(targets):
    ''' UI prompts for mutilatotion target and target area and returns a pair. '''
    return ui.night_mutilator_vote(targets)


def get_doctor_target(targets):
    ''' UI prompts for doctor target and returns their name. '''
    return ui.night_doctor_vote(targets)
