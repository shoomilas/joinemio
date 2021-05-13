import gym
import enum
import random
import logging as log
import numpy as np
from gym.spaces import Discrete, Box
from Board import Game, Board, GameState


class RandomPlayer:
    def get_action(self, board_state):
        return random.choice(self.possible_moves(board_state))

    @staticmethod
    def possible_moves(board_state):
        available_cols = []
        for i in range(len(board_state[0])):
            if board_state[0][i] == 0:
                available_cols.append(i)
        return available_cols


class AIPlayer:
    def get_action(self, board_state, my_token):  # TODO
        pass


class Reward(enum.Enum):
    win = 100
    loss = -100
    draw = 1
    not_end = 0


class ConnectFourEnv(gym.Env):
    def __init__(self):
        self.game = Game()
        self.action_space = Discrete(7)
        self.observation_space = Box(low=0, high=2, shape=Board.shape, dtype=np.ushort)

    def play_one_game(self, player1_main, player2_opponent):
        players = [player1_main, player2_opponent]
        self.observation_space = self.reset()
        while not self.game.game_state == GameState.finished:
            self.observation_space, reward, done, info = \
                self.step(players[self.game.current_player-1].get_action(self.observation_space))
        log.debug(
            f"Winner: {self.game.winner}"
        )
        return self.observation_space, reward, done, info  # reward for player1

    def step(self, action):  # close to move from Game class
        self.game.move(action)  # switching player if game not ended
        if self.game.game_state == GameState.finished:
            if self.game.winner == 1:
                return self.observation_space, Reward.win, self.game.game_state, {}
            elif self.game.winner == 2:
                return self.observation_space, Reward.loss, self.game.game_state, {}
            else:
                return self.observation_space, Reward.draw, self.game.game_state, {}
        else:
            return self.observation_space, Reward.not_end, self.game.game_state, {}  # not end

    def reset(self):
        self.game = Game()
        return self.game.board.grid

    def render(self, mode: str = 'console', close: bool = False) -> None:
        print(self.game.board.grid)


def main():
    env = ConnectFourEnv()
    rand1 = RandomPlayer()
    rand2 = RandomPlayer()
    for i in range(100):
        env.play_one_game(rand1, rand2)
        env.render()
        if env.game.winner is None:
            exit(0)
        env.reset()


if __name__ == "__main__":
    main()
