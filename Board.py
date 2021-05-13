import numpy as np
import itertools
import logging as log

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
                return result
        return 0
    
    def check_result_horizontal(self): # TODO
        log.debug(f"HORIZONTAL CHECK")
        for row in range(self.rows):
            current_row_vec = self.grid[row]
            self.check_sequence(current_row_vec)
        return 0
    
    def check_result_diagonal(self): # TODO
        log.debug("DIAGONAL CHECK")
        for diag in range(self.columns):
            if len(self.grid.diagonal(diag)) > self.winning_sequence_length: 
                self.check_sequence(self.grid.diagonal(diag))
            if len(self.grid.diagonal(-diag)) > self.winning_sequence_length: 
                self.check_sequence(self.grid.diagonal(-diag))
        flipped_grid = np.fliplr(self.grid)
        for diag in range(self.columns):
            if len(flipped_grid.diagonal(diag)) > self.winning_sequence_length: 
                self.check_sequence(flipped_grid.diagonal(diag))
            if len(flipped_grid.diagonal(-diag)) > self.winning_sequence_length:
                self.check_sequence(flipped_grid.diagonal(-diag))
        # TODO: DRY
        return 0

    def check_result(self):
        result = self.check_result_vertical() or self.check_result_horizontal() or self.check_result_diagonal()
        if (result == True): 
            return GameState.finished


# class Game: # TODO
    # def move():
    #     if: drop_token(bleble, current_player)
    #     else: repeat_try
    #     win_check()

# class Render(): # TODO


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
    bo.drop_token(1,1)
    bo.drop_token(2,1)
    bo.drop_token(3,1)
    bo.drop_token(4,1)
    bo2.check_result()

    
    # log.debug("======")

    


if __name__ == "__main__":
    main()