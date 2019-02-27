''' Facade for getting input. '''
import Io.release_io as rlio
import Io.debug_io as dbgio
import Io.logger as logger

def get_player_cnt():
    if logger.is_debug_mode():
        return dbgio.get_player_cnt()
    else:
        return rlio.get_player_cnt()


def get_names_emails(role_list, player_cnt, player_data):
    if logger.is_debug_mode():
        return dbgio.get_names_emails(role_list, player_cnt, player_data)
    else:
        return rlio.get_names_emails(role_list, player_cnt, player_data)


def get_lynched_name(can_vote, still_alive):
    if logger.is_debug_mode():
        return dbgio.get_lynched_name()
    else:
        return rlio.get_lynched_name(can_vote, still_alive)


def get_assn_target(player_data, targets):
    if logger.is_debug_mode():
        return dbgio.get_assn_target(player_data)
    else:
        return rlio.get_assn_target(targets)

def get_police_target(player_data, targets):
    if logger.is_debug_mode():
        return dbgio.get_police_target(player_data)
    else:
        return rlio.get_police_target(targets)


def show_police_answer(player_data, target):
    if logger.is_debug_mode():
        return dbgio.show_police_answer(player_data, target)
    else:
        return rlio.show_police_answer(player_data, target)


def get_mutilator_target(player_data, targets):
    if logger.is_debug_mode():
        return dbgio.get_mutilator_target(player_data)
    else:
        return rlio.get_mutilator_target(targets)


def get_doctor_target(player_data, targets):
    if logger.is_debug_mode():
        return dbgio.get_mutilator_target(player_data)
    else:
        return rlio.get_mutilator_target(targets)
