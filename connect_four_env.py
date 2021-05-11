import gym
import enum
import random
from gym.spaces import Discrete, Box
import numpy as np


class RandomPlayer:
    def get_action(self, board_state, my_token):
        return random.choice(possible_moves(board_state))


class AIPlayer:
    def get_action(self, board_state, my_token):
        ...

class Reward(enum.Enum):
    win = 100
    loss = -100
    draw = 1
    not_end = 0

class ConnectFourEnv(gym.Env):
    def __init__(self):
        self.action_space = Discrete(7)
        self.observation_space = Box(low=0, high=2, shape=(6, 7), dtype=np.integer)
        self._board_state = np.zeros((6, 7), dtype=int)
        self._current_player = 1

    def play_one_game(self, player1, player2):
        self.reset()
        done = False
        while not done:
            if self._current_player == 1:
                self._board_state, reward, done, info = self._step(player1.get_action(self._board_state, 1))
                self._current_player = 2
            else:
                self._board_state, reward, done, info = self._step(player2.get_action(self._board_state, 2))
                self._current_player = 1
        return self._board_state, reward, done, info

    def _step(self, action):
        board_state = drop_piece(self._board_state, action)  # function that drops one piece in chosen column
        reward = self.step_result()
        if reward == Reward.not_end:
            return board_state, reward, False, {}  # game not ended
        elif reward == Reward.win:
            if self._current_player == 1:
                return board_state, reward, True, {}  # player1 wins
            else:
                return board_state, -reward, True, {}  # player2 wins
        else:
            return board_state, reward, True, {}  # draw

    def step_result(self):
        if end_state(self._board_state):  #some function
            if win_state(self._board_state):  #some function
                return Reward.win
            else:
                return Reward.draw
        else:
            return Reward.not_end

    def reset(self):
        self._board_state = np.zeros((6, 7), dtype=int)
        return self.state
    
    def render(self):
        draw_pieces_in_window(self._board_state)
