import random
from sys import exit
import whist_api.io_api.facade_io as io
from whist_api.io_api.whist_logger import WhistLogger as Logger

class GameState:
    LOGGER = None

    def __init__(self, logger, player_cnt, player_names):
        ''' Creates initial game state. '''
        LOGGER = logger
        if player_cnt < 3 or player_cnt > 6:
            logger.log_debug('There can only be 4, 5 or 6 players.')
            sys.exit()

        self.names = player_names
        self.player_cnt = player_cnt
        self.dealer = random.randint(0, player_cnt - 1)
        self.card_cnt = 1
        self.round = 0

        round_cnt = 3 * player_cnt + 12
        # Blank matrix
        self.bid_history = [[0 for i in range(player_cnt)] for j in range(round_cnt)]
        self.result_history = self.bid_history
        self.scoreboard = self.bid_history
        self.point_diff = self.bid_history


    def _get_player_from_ord(self, player_ord):
        ''' Returns the actual index of the n-th player in the current round.
        '''
        return (self.dealer + player_ord) % self.player_cnt


    def _prev_score(self, round, player_name):
        ''' Returns score that new points are to be added to. '''
        if (round == 0):
            return 0

        return self.scoreboard[round - 1][player_name]


    def _update_scoreboard(self, round):
        ''' Updates scoreboard information after a round was played. '''
        for player_idx in range(self.player_cnt):
            # Player made their contract
            bid = self.bid_history[round][player_idx]
            result = self.result_history[round][player_idx]
            if bid == result:
                point_diff[round][player_idx] = 5 + bid
            else:
                point_diff[round][player_idx] = - abs(bid - result)
            
            self.scoreboard[round][player_idx] = self._prev_score(round, player_idx) + point_diff


    def play_bids(self):
        ''' Gets bids from input. '''
        bid_sum = 0
        for player_ord in range(1, player_cnt):
            player_idx = self._get_player_from_ord(player_ord)
            bid_history[self.round][player_idx] = io.get_bid(self.names[player_idx], bids)
            bid_sum += bid[player_idx]

        # Dealer's bid is constrained by other bids
        dealer_bids = []
        for j in range(0, self.card_cnt + 1):
            if bid_sum + j != self.card_cnt:
                dealer_bids.append(j)

        bid_history[self.round][self.dealer] = io.get_bid(self.names[self.dealer], dealer_bids)


    def get_results(self):
        # logger.log_info('Enter results!')
        possible_results = [i for i in range(0, self.card_cnt + 1)]
        for player_ord in range(0, player_cnt + 1):
            player_idx = self._get_player_from_ord(player_ord)
            self.result_history[player_idx] = io.get_result(player_names[player_idx], possible_results)


    def advance_round(self, player_bids, player_results):
        ''' Updates scoreboard, cards in the round and round counter. '''
        self.dealer =  (self.dealer + 1) % player_cnt

        # 0 1 ...  p-1         p+5         2*p+5       2*p+11
        # 1 1 ... [1 2 3 4 5 6 7] 8 8 ... [8 7 6 5 4 3 2] 1 1 ... 1
        if self.round >= player_cnt - 1 and self.round <= player_cnt + 5:
            self.card_cnt += 1
        elif self.round >= 2 * player_cnt + 5 and self.round <= 2 * p + 11:
            self.card_cnt -= 1

        self._update_scoreboard()
        io.show_scoreboard(self.player_cnt, self.player_names, self.round, self.scoreboard)

        self.round += 1
