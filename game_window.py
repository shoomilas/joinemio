import logging as log
import numpy as np

from board import Game
from board import Board
from board import GameState
from pyglet import gl
from pyglet import graphics
from pyglet.window import Window
from pyglet.window import mouse
from math import sin, cos, pi


class GameWindow:
    refresh_rate = 1 / 2
    column_width = row_height = 100
    black_color = (0, 0, 0, 0)
    red_color = (255, 0, 0, 0)
    blue_color = (0, 0, 255, 0)
    green_color = (0, 255, 0, 0)
    grid_color = green_color
    player_one_color = red_color
    player_two_color = blue_color
    piece_radius = row_height * 0.4
    win_width = 7 * column_width
    win_height = 6 * row_height

    def __init__(self, game=None):  # could move outside
        self.game = game
        if game is None:
            self.game = Game()
        self.win_width = self.game.board.columns * self.column_width
        self.win_height = self.game.board.rows * self.row_height
        self.window = Window(
            width=self.win_width, height=self.win_height
        )  # ,visible=False)
        self.on_draw = self.window.event(self.on_draw)
        self.on_mouse_press = self.window.event(self.on_mouse_press)

    def on_draw(self):
        self.window.clear()
        self.draw_grid()
        self.draw_all_pieces()

    def on_mouse_press(self, x, y, button, modifiers):
        # global game.last_column_clicked
        if self.game.game_state == GameState.finished:
            return
        column_clicked = x // self.column_width
        if button == mouse.LEFT:
            self.game.move(column_clicked)

    def update(self, dt):
        if self.game.game_state == GameState.finished:
            return
        log.debug(f"Current game.board.grid state: \n{self.game.board.grid}")

    def draw_all_pieces(self):
        for index, x in np.ndenumerate(self.game.board.grid):
            if x == 1:
                self.draw_piece(index[1], 5 - index[0], self.player_one_color)
            if x == 2:
                self.draw_piece(index[1], 5 - index[0], self.player_two_color)

    def draw_piece(self, x, y, color=(255, 255, 255, 0)):
        self.draw_reg_polygon(
            x * GameWindow.column_width + GameWindow.column_width // 2,
            y * GameWindow.row_height + GameWindow.row_height // 2,
            GameWindow.piece_radius,
            64,
            color,
        )

    def draw_reg_polygon(self, x, y, r, n, color=(255, 255, 255, 0)):
        vertices = []
        th = 0
        for _ in range(n):
            vertices += [x + r * sin(th), y + r * cos(th)]
            th += 2 * pi / n
        graphics.draw(n, gl.GL_POLYGON, ("v2f", vertices), ("c4B", color * n))

    def draw_grid(self):
        for i in range(self.game.board.columns):
            self.draw_line(
                i * self.row_height,
                0,
                i * self.row_height,
                self.win_height,
                color=GameWindow.grid_color,
            )
        for i in range(self.game.board.rows):
            self.draw_line(
                0,
                i * GameWindow.column_width,
                GameWindow.win_width,
                i * GameWindow.column_width,
                color=GameWindow.grid_color,
            )

    def draw_line(self, x1, y1, x2, y2, color=(255, 255, 255, 0)):
        graphics.draw(2, gl.GL_LINES, ("v2i", (x1, y1, x2, y2)), ("c4B", color * 2))
