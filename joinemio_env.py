import gym
from gym import error, spaces, utils
from gym.utils import seeding
 
import enum
import random
import logging as log
import numpy as np
from gym.spaces import Discrete, Box
from board import Game, Board, GameState
from game_window import GameWindow
from pyglet import clock
from pyglet import app

class JonemioEnv(gym.Env):
  metadata = {'render.modes': ['human']}

  def __init__(self):
    self.game = Game()
    self.action_space = Discrete(7)
    self.observation_space = Box(low=0, high=2, shape=Board.shape, dtype=np.ushort)

  def step(self, action):
    ...
  def reset(self):
    self.game = Game()
    return self.game.board.grid
  def render(self, mode='human'):
    ...
  def close(self):
    ...