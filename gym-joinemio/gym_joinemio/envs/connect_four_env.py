import gym
import enum
import logging as logging
import numpy as np
import random

from collections import namedtuple, deque
from gym_joinemio.envs.player import RandomPlayer, AIPlayer
from gym_joinemio.envs.board import Game, Board, GameState
from gym_joinemio.envs.game_window import GameWindow
from gym.spaces import Discrete, Box
from pyglet import clock
from pyglet import app

logging.getLogger("gym_joinemio.envs.board").setLevel(logging.CRITICAL)
log = logging.getLogger(__name__)


class GameWindowForBots(GameWindow):
    def __init__(
        self, game=None, player1_main=RandomPlayer(), player2_opponent=RandomPlayer()
    ):
        super().__init__(game)
        self.players = [player1_main, player2_opponent]

    def update_for_bots(self, dt):
        if self.game.game_state == GameState.finished:
            return
        self.game.move(
            self.players[self.game.current_player - 1].get_action(self.game.board.grid)
        )
        log.debug(f"Current game.board.grid state: \n{self.game.board.grid}")


class Reward(enum.Enum):
    win = 1
    loss = -10
    draw = -1
    not_end = 1/42


Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))


class ReplayMemory(object):
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class ConnectFourEnv(gym.Env):
    def __init__(self):
        self.game = Game()
        board_width = Board.shape[1]
        self.action_space = Discrete(board_width)
        self.recording = []  # (player, move, reward for move)
        self.observation_space = Box(low=0, high=2, shape=Board.shape, dtype=np.ushort)

    def rewarder(
        self,
    ):  # Could make it into __init__ parameter / make it configurable with another method
        if self.game.game_state == GameState.finished:
            if self.game.winner == 1:
                return Reward.win
            elif self.game.winner == 2:
                return Reward.loss
            else:
                return Reward.draw
        else:
            return Reward.not_end

    def play_one_game(self, player1_main, player2_opponent, each_step_render=False):
        if each_step_render:
            self.observation_space = self.reset()
            window = GameWindowForBots(self.game, player1_main, player2_opponent)
            clock.schedule_interval(window.update_for_bots, GameWindow.refresh_rate)
            app.run()
        else:
            players = [player1_main, player2_opponent]
            self.observation_space = self.reset()
            action = None
            while not self.game.game_state == GameState.finished:
                current_player = self.game.current_player - 1
                action = players[current_player].get_action(self.observation_space)
                self.observation_space, reward, done, info = self.step(action)
                self.recording.append((current_player + 1, action, self.rewarder()))
            log.debug(f"Winner: {self.game.winner}")
            return self.observation_space, reward, done, info  # reward for player1

    def step(self, action):  # close to move from Game class
        self.game.move(action)  # switching player if game not ended
        return (
            self.observation_space,
            self.rewarder(),
            self.game.game_state,
            {},
        )  # not end

    def reset(self):
        self.game = Game()
        return self.game.board.grid

    def render(self, mode: str = "human", close: bool = False) -> None:
        if mode == "console":
            print(self.game.board.grid)
        elif mode == "human":
            window = GameWindow(self.game)
            clock.schedule_interval(window.update, GameWindow.refresh_rate)
            app.run()
        else:
            print("Only console and human render modes supported")


def main():
    env = ConnectFourEnv()
    player1 = RandomPlayer()
    player2 = RandomPlayer()

    for i in range(10):
        one_game = env.play_one_game(player1, player2, each_step_render=False)
        log.info(one_game)
        env.render()  # Will cause showing the result board. mode = 'console' parameter ditches the UI rendering


if __name__ == "__main__":
    main()
