import gym
import enum
import logging as logging
import numpy as np
from player import RandomPlayer, AIPlayer
from gym.spaces import Discrete, Box
from board import Game, Board, GameState
from game_window import GameWindow
from pyglet import clock
from pyglet import app

logging.getLogger("board").setLevel(logging.CRITICAL)
log = logging.getLogger(__name__)



class GameWindowForBots(GameWindow):
    def __init__(self, game=None, player1_main=RandomPlayer(), player2_opponent=RandomPlayer()):
        super().__init__(game)
        self.players = [player1_main, player2_opponent]

    def update_for_bots(self, dt):
        if self.game.game_state == GameState.finished:
            return
        self.game.move(self.players[self.game.current_player-1].get_action(self.game.board.grid))
        log.debug(f"Current game.board.grid state: \n{self.game.board.grid}")

class Reward(enum.Enum):
    win = 100
    loss = -100
    draw = 1
    not_end = 0


class ConnectFourEnv(gym.Env):
    def __init__(self):
        self.game = Game()
        board_width = Board.shape[1]
        self.action_space = Discrete(board_width)
        self.observation_space = Box(low=0, high=2, shape=Board.shape, dtype=np.ushort)

    def play_one_game(self, player1_main, player2_opponent, each_step_render=False):
        if each_step_render:
            self.observation_space = self.reset()
            window = GameWindowForBots(self.game, player1_main, player2_opponent)
            clock.schedule_interval(window.update_for_bots, GameWindow.refresh_rate)
            app.run()
        else:
            players = [player1_main, player2_opponent]
            self.observation_space = self.reset()
            while not self.game.game_state == GameState.finished:
                self.observation_space, reward, done, info = self.step(players[self.game.current_player-1].get_action(self.observation_space))
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

    def render(self, mode: str = 'human', close: bool = False) -> None:
        if mode == 'console':
            print(self.game.board.grid)
        elif mode == 'human':
            window = GameWindow(self.game)
            clock.schedule_interval(window.update, GameWindow.refresh_rate)
            app.run()
        else:
            print("Only console and human render modes supported")


def main():
    env = ConnectFourEnv()
    player1 = RandomPlayer()
    player2 = RandomPlayer()
    
    for i in range(100):
        env.play_one_game(player1, player2, each_step_render=False)  # Plays the game
        # env.render() # Will cause showing the result board
        env.render(mode = 'console')
    # env.play_one_game(player1, player2, each_step_render=True) # each_step_render to see the gameplay


if __name__ == "__main__":
    main()