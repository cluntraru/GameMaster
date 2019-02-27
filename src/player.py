class Player:
    _PLAYER_IDX = 0
    _ASSN_IDX = 1
    _POLICE_IDX = 2
    _SUICD_IDX = 3
    _DOCTOR_IDX = 4
    _MTLT_IDX = 5
    _POTATO_IDX = 6

    _ROLE_NAMES = ['ERROR', 'assassin', 'policeman', 'suicidal person',\
                      'doctor', 'mutilator', 'townie']

    def __init__(self, role_idx):
        self._role_idx = role_idx
        self._alive = True
        self._can_vote = True

    def get_alive(self):
        ''' Returns if the player is alive. '''
        return self._alive

    
    def die(self):
        ''' Removes the player from the game. '''
        self._alive = False

    
    def get_can_vote(self):
        ''' Returns if player can vote at the current moment. '''
        return self._can_vote

    
    def set_can_vote(self, can_vote):
        ''' Sets if a player can vote. '''
        self._can_vote = can_vote


    def get_role_idx(self):
        ''' Returns index of role. '''
        return self._role_idx


    def get_role_name(self):
        ''' Converts a role index constant to the actual role name.'''
        return Player._ROLE_NAMES[self._role_idx]


    def is_assn(self):
        ''' Returns if player is an assassin. '''
        return self._role_idx == self._ASSN_IDX


    def is_police(self):
        ''' Returns if player is a policeman. '''
        return self._role_idx == self._POLICE_IDX


    def is_suicidal(self):
        ''' Returns if player is a suicidal person. '''
        return self._role_idx == self._SUICD_IDX


    def is_doctor(self):
        ''' Returns if player is a doctor. '''
        return self._role_idx == self._DOCTOR_IDX


    def is_mutilator(self):
        ''' Returns if player is a mutilator. '''
        return self._role_idx == self._MTLT_IDX


    def is_potato(self):
        ''' Returns if player is a townie. '''
        return self._role_idx == self._POTATO_IDX
