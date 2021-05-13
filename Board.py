import numpy as np
import itertools
import logging as log

from pyglet import app
from pyglet import clock
from pyglet import gl
from pyglet import graphics
from pyglet.window import Window
from pyglet.window import mouse
from math import sin, cos, pi


LOG_LEVEL = log.DEBUG
LOG_FORMAT = "[%(levelname)s] %(message)s"
log.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)


class GameState:
    finished = True
    ongoing = False


class Board:
    columns = 7
    rows = 6
    shape = (rows, columns)
    empty = 0
    winning_sequence_length = 4

    def fill_grid(self):  # TODO: REMOVE
        a = 0
        riter = np.nditer(self.grid, flags=["multi_index"])
        for x in riter:
            self.grid[riter.multi_index] = a
            a += 1

    def __init__(self):
        self.grid = np.zeros(Board.shape, dtype=np.ushort)
        self.game_over = False

    def drop_token(self, column_no, player) -> bool:
        """Returns True on successful move, False when column is full."""
        column_vector_reversed = list(enumerate(self.grid[:, column_no]))[::-1]
        for i, val in column_vector_reversed:
            if val == Board.empty:
                self.grid[i, column_no] = player
                return True
        return False

    def check_sequence(self, vector, seq_length=None):  # TODO
        """Return 0 if sequence not found or if found: a value of the element that the seq of was found"""
        if seq_length == None:
            seq_length = self.winning_sequence_length
        for key, group in itertools.groupby(vector):
            current_group = list(group)
            if key != Board.empty and len(current_group) >= seq_length:
                first_element = current_group[0]
                log.debug(
                    f"Found winning group of element {first_element}: {current_group} for vector: {vector}"
                )
                return first_element
        log.debug(f"Did not find a winning group of any element for vector: {vector}")
        return Board.empty

    def check_result_vertical(self):  # TODO
        log.debug(f"VERTICAL CHECK")
        for col in range(self.columns):
            current_column_vec = self.grid[:, col]
            result = self.check_sequence(current_column_vec)
            if result != 0:
                return True
        return False

    def check_result_horizontal(self):  # TODO
        log.debug(f"HORIZONTAL CHECK")
        for row in range(self.rows):
            current_row_vec = self.grid[row]
            result = self.check_sequence(current_row_vec)
            if result != 0:
                return True
        return False

    def check_result_diagonal(self):  # TODO
        log.debug("DIAGONAL CHECK")
        for diag in range(self.columns):
            if len(self.grid.diagonal(diag)) > self.winning_sequence_length:
                result = self.check_sequence(self.grid.diagonal(diag))
                if result != 0:
                    return True
            if len(self.grid.diagonal(-diag)) > self.winning_sequence_length:
                result = self.check_sequence(self.grid.diagonal(-diag))
                if result != 0:
                    return True
        flipped_grid = np.fliplr(self.grid)
        for diag in range(self.columns):
            if len(flipped_grid.diagonal(diag)) > self.winning_sequence_length:
                result = self.check_sequence(flipped_grid.diagonal(diag))
                if result != 0:
                    return True
            if len(flipped_grid.diagonal(-diag)) > self.winning_sequence_length:
                result = self.check_sequence(flipped_grid.diagonal(-diag))
                if result != 0:
                    return True
        return False

    def check_result(self):
        result = (
            self.check_result_vertical()
            or self.check_result_horizontal()
            or self.check_result_diagonal()
        )
        if result != 0:
            return GameState.finished
        return GameState.ongoing


class Game:  # TODO
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.game_state = GameState.ongoing
        self.winner = None

    def switch_player(self):
        self.current_player = (self.current_player % 2) + 1

    def move(self, column):
        if self.board.drop_token(column, self.current_player):
            game_result = self.board.check_result()
            if game_result == GameState.finished:
                self.winner = self.current_player
                self.game_state = game_result
            else:
                self.switch_player()
        else:
            pass  # repeat move


class GameWindow():  # TODO
    refresh_rate = 1/2
    column_width = row_height = 100
    black_color = (0, 0, 0, 0)
    red_color = (255, 0, 0, 0)
    blue_color = (0, 0, 255, 0)
    green_color = (0,255,0,0)
    grid_color = green_color
    player_one_color = red_color
    player_two_color = blue_color
    piece_radius = row_height * 0.4
    win_width = 7 * column_width
    win_height = 6 * row_height

    def __init__(self, game=None):  # could move outside
        self.game = game
        if game == None:
            self.game = Game()
        self.win_width = self.game.board.columns * self.column_width
        self.win_height = self.game.board.rows * self.row_height
        self.window = Window(width=self.win_width, height=self.win_height)  # ,visible=False)
        self.on_draw = self.window.event(self.on_draw)
        self.on_mouse_press = self.window.event(self.on_mouse_press)

    def on_draw(self):
        self.window.clear()
        self.draw_grid()
        self.draw_all_pieces()

    def on_mouse_press(self, x, y, button, modifiers):
    # global game.last_column_clicked
        if(self.game.game_state == GameState.finished):
            return
        column_clicked = x // self.column_width 
        if button == mouse.LEFT:
            self.game.move(column_clicked)

    def update(self, dt):
        if(self.game.game_state == GameState.finished):
            return
        log.debug(f"Current game.board.grid state: \n{self.game.board.grid}")

    def draw_all_pieces(self):
        for index, x in np.ndenumerate(self.game.board.grid):
            if x == 1:
                self.draw_piece(index[1], 5-index[0], self.player_one_color)
            if x == 2:
                self.draw_piece(index[1],  5-index[0], self.player_two_color)

    def draw_piece(self, x, y, color=(255, 255, 255, 0)):
        self.draw_reg_polygon(x * GameWindow.column_width + GameWindow.column_width // 2, y * GameWindow.row_height + GameWindow.row_height // 2, GameWindow.piece_radius, 64, color)

    def draw_reg_polygon(self, x, y, r, n, color=(255, 255, 255, 0)):
        vertices = []
        th = 0
        for _ in range(n):
            vertices += [x + r * sin(th), y + r * cos(th)]
            th += 2 * pi / n
        graphics.draw(n, gl.GL_POLYGON, ('v2f', vertices), ('c4B', color * n))

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


def main():
    bo = Board()
    log.debug(bo.grid)
    # log.debug("======")
    log.debug(bo.drop_token(3, 1))
    log.debug(bo.drop_token(3, 2))
    log.debug(bo.drop_token(3, 2))
    # log.debug( bo.drop_token(3,2) )
    log.debug(bo.drop_token(3, 2))
    bo2 = Board()
    bo2.drop_token(1, 1)
    bo2.drop_token(2, 1)
    bo2.drop_token(3, 1)
    bo2.drop_token(4, 1)
    bo2.check_result()


# def main_render():
#     r = Render()


if __name__ == "__main__":
    window = GameWindow()
    clock.schedule_interval(window.update, GameWindow.refresh_rate)
    app.run()
