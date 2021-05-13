import numpy as np
import itertools
import logging as log

from pyglet import app
from pyglet import clock
from pyglet import gl
from pyglet import graphics
import pyglet
from pyglet.window import Window
from pyglet.window import mouse
from math import sin, cos, pi


LOG_LEVEL = log.DEBUG
LOG_FORMAT = "[%(levelname)s] %(message)s"
log.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)

class GameState:
    finished=True
    ongoing=False

class Board:
    columns = 7
    rows = 6
    shape = (rows, columns)
    empty = 0
    winning_sequence_length = 4
    
    def fill_grid(self): # TODO: REMOVE
        a = 0
        riter = np.nditer(self.grid, flags=['multi_index'])
        for x in riter:
            self.grid[riter.multi_index] = a
            a += 1

    def __init__(self):
        self.grid = np.zeros(Board.shape, dtype=np.ushort)
        # self.fill_grid() # TODO: Remove

        self.game_over = False

    def drop_token(self, column_no, player) -> bool:
        ''' Returns True on successful move, False when column is full. '''
        column_vector_reversed = list(enumerate(self.grid[:,column_no]))[::-1]
        for i, val in column_vector_reversed:
            if(val == Board.empty): 
                self.grid[i,column_no]=player
                return True
        return False

    def check_sequence(self, vector, seq_length=None): # TODO
        ''' Return 0 if sequence not found or if found: a value of the element that the seq of was found '''
        if seq_length == None: seq_length = self.winning_sequence_length
        for key, group in itertools.groupby(vector):
            current_group = list(group)
            if (key != Board.empty and len(current_group) >= seq_length):
                first_element = current_group[0]
                log.debug(f"Found winning group of element {first_element}: {current_group} for vector: {vector}")
                return first_element
        log.debug(f"Did not find a winning group of any element for vector: {vector}")
        return Board.empty

    def check_result_vertical(self): # TODO
        log.debug(f"VERTICAL CHECK")
        for col in range(self.columns):
            current_column_vec=self.grid[:,col]
            result = self.check_sequence(current_column_vec)
            if result != 0:
                return True
        return False
    
    def check_result_horizontal(self): # TODO
        log.debug(f"HORIZONTAL CHECK")
        for row in range(self.rows):
            current_row_vec = self.grid[row]
            result = self.check_sequence(current_row_vec)
            if result != 0: return True
        return False
    
    def check_result_diagonal(self): # TODO
        log.debug("DIAGONAL CHECK")
        for diag in range(self.columns):
            if len(self.grid.diagonal(diag)) > self.winning_sequence_length: 
                result = self.check_sequence(self.grid.diagonal(diag))
                if result != 0: return True
            if len(self.grid.diagonal(-diag)) > self.winning_sequence_length: 
                result = self.check_sequence(self.grid.diagonal(-diag))
                if result != 0: return True
        flipped_grid = np.fliplr(self.grid)
        for diag in range(self.columns):
            if len(flipped_grid.diagonal(diag)) > self.winning_sequence_length: 
                result = self.check_sequence(flipped_grid.diagonal(diag))
                if result != 0: return True
            if len(flipped_grid.diagonal(-diag)) > self.winning_sequence_length:
                result = self.check_sequence(flipped_grid.diagonal(-diag)) 
                if result != 0: return True
        return False

    def check_result(self):
        result = self.check_result_vertical() or self.check_result_horizontal() or self.check_result_diagonal()
        if (result != 0): 
            return GameState.finished
        return GameState.ongoing


class Game: # TODO
    def __init__(self):
        self.board = Board()
        self.current_player = 1
        self.game_state = GameState.ongoing
        self.winner = None

    def switch_player(self): 
        self.current_player = (self.current_player % 2) + 1

    def move(self, column):
        if (self.board.drop_token(column, self.current_player)):
            game_result = self.board.check_result()
            if (game_result == GameState.finished):
                self.winner = self.current_player
                self.game_state = game_result
            else:
                self.switch_player()
        else: 
            pass # repeat move
class Render(): # TODO
    column_width = row_height = 100
    
    def __init__(self, game = None): # could move outside 
        self.game = game
        if game == None: self.game = Game()
        win_width = self.game.board.columns * self.column_width
        win_height = self.game.board.rows * self.row_height
        self.window = Window(width=win_width, height=win_height) # ,visible=False)

    # @self.window.event # TODO
    # def on_draw(self):
    #     window.clear()
    #     draw_grid()
    #     draw_all_pieces()

    # @window.event # TODO
    # def on_mouse_press(x, y, button, modifiers):

    def draw_all_pieces(): pass
    def draw_grid(): pass
    def draw_piece(): pass
    def draw_reg_polygon(): pass
    def draw_line(): pass


def main():
    bo = Board()
    log.debug(bo.grid)
    # log.debug("======")
    log.debug( bo.drop_token(3,1) )
    log.debug( bo.drop_token(3,2) )
    log.debug( bo.drop_token(3,2) )
    # log.debug( bo.drop_token(3,2) )
    log.debug( bo.drop_token(3,2) )

    a = np.array([0,1,1,1,0,1,1,0,0,1,2,])
    b = np.array([0,1,2,1,0,1,1,1,1,1,2,])
    # bo.check_sequence(bo.grid[:,3], 4)
    # log.debug("======")
    # log.debug(bo.check_sequence(b, 4))
    # bo.check_sequence(a, 4)
    bo.check_result()
    log.debug("======")

    bo2 = Board()
    bo2.drop_token(1,1)
    bo2.drop_token(2,1)
    bo2.drop_token(3,1)
    bo2.drop_token(4,1)
    bo2.check_result()
    
    # log.debug("======")


def main_render():
    r = Render()


if __name__ == "__main__":
    main_render()
    # main()