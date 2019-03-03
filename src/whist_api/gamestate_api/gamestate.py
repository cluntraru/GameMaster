''' GameState class implementation. '''
import random
import sys
import whist_api.io_api.facade_io as io

class GameState:
    ''' GameState class. Multiple instances can be created for testing. '''
    LOGGER = None

    def __init__(self, logger, player_cnt, player_names):
        ''' Creates initial game state. '''
        GameState.LOGGER = logger
        if player_cnt < 3 or player_cnt > 6:
            logger.log_debug('There can only be 4, 5 or 6 players.')
            sys.exit()

        self._names = player_names
        self._player_cnt = player_cnt
        self._dealer = random.randint(0, player_cnt - 1)
        self._card_cnt = 1
        self._round = 0
        self._round_cnt = 3 * player_cnt + 12

        # Blank matrix
        self._bid_history = [[0 for i in range(player_cnt)] for j in range(self._round_cnt)]
        self._result_history = [[0 for i in range(player_cnt)] for j in range(self._round_cnt)]
        self._scoreboard = [[0 for i in range(player_cnt)] for j in range(self._round_cnt)]
        self._point_diff = [[0 for i in range(player_cnt)] for j in range(self._round_cnt)]


    def _get_player_from_ord(self, player_ord):
        ''' Returns the actual index of the n-th player in the current round.
        '''
        return (self._dealer + player_ord) % self._player_cnt


    def _prev_score(self, target_round, player_name):
        ''' Returns score that new points are to be added to. '''
        if target_round == 0:
            return 0

        return self._scoreboard[target_round - 1][player_name]


    def _update_scoreboard(self, target_round):
        ''' Updates scoreboard information after a round was played. '''
        for player_idx in range(self._player_cnt):
            # Player made their contract
            # print(self._bid_history, curr_round, player_idx)
            bid = self._bid_history[target_round][player_idx]
            result = self._result_history[target_round][player_idx]
            if bid == result:
                point_diff = 5 + bid
            else:
                point_diff = - abs(bid - result)

            self._point_diff[target_round][player_idx] = point_diff

            new_score = self._prev_score(target_round, player_idx) + point_diff
            self._scoreboard[target_round][player_idx] = new_score


    def _play_bids(self):
        ''' Gets bids from input. '''
        bid_sum = 0
        possible_bids = [i for i in range(0, self._card_cnt + 1)]
        for player_ord in range(1, self._player_cnt):
            player_idx = self._get_player_from_ord(player_ord)
            curr_bid = io.get_bid(GameState.LOGGER, self._names[player_idx], possible_bids)
            self._bid_history[self._round][player_idx] = curr_bid
            bid_sum += curr_bid

        # Dealer's bid is constrained by other bids
        possible_dealer_bids = []
        for j in range(0, self._card_cnt + 1):
            if bid_sum + j != self._card_cnt:
                possible_dealer_bids.append(j)

        dealer_bid = io.get_bid(GameState.LOGGER, self._names[self._dealer], possible_dealer_bids)
        self._bid_history[self._round][self._dealer] = dealer_bid


    def _play_results(self):
        possible_results = [i for i in range(0, self._card_cnt + 1)]
        for player_ord in range(1, self._player_cnt):
            player_idx = self._get_player_from_ord(player_ord)
            player_result = io.get_result(GameState.LOGGER,\
                                          self._names[player_idx], possible_results)

            self._result_history[self._round][player_idx] = player_result

        dealer_result = io.get_result(GameState.LOGGER, self._names[self._dealer],\
                                      possible_results)

        self._result_history[self._round][self._dealer] = dealer_result


    def _advance_round(self):
        ''' Updates scoreboard, cards in the round and round counter. '''
        self._dealer = (self._dealer + 1) % self._player_cnt

        # 0 1 ...  p-1         p+5         2*p+5       2*p+11
        # 1 1 ... [1 2 3 4 5 6 7] 8 8 ... [8 7 6 5 4 3 2] 1 1 ... 1
        if self._round >= self._player_cnt - 1 and self._round <= self._player_cnt + 5:
            self._card_cnt += 1
        elif self._round >= 2 * self._player_cnt + 5 and self._round <= 2 * self._player_cnt + 11:
            self._card_cnt -= 1

        self._update_scoreboard(self._round)
        io.show_scoreboard(GameState.LOGGER, self._player_cnt, self._names,\
                           self._round, self._scoreboard, self._point_diff)

        self._round += 1


    def _play_round(self):
        ''' Plays the next round in the game. '''
        GameState.LOGGER.log_info('Round ' + str(self._round + 1))
        GameState.LOGGER.log_info('Dealer: ' + self._names[self._dealer])
        self._play_bids()
        self._play_results()
        self._advance_round()


    def _game_over(self):
        ''' Checks if there are any rounds left in the game. '''
        return self._round == self._round_cnt


    def start_game(self):
        ''' Starts a game of Whist. '''
        while not self._game_over():
            self._play_round()
