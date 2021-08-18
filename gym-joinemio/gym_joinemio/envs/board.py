import itertools
import logging as logging
import numpy as np

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = "[%(levelname)s][%(module)s|%(name)s] %(message)s"
logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
log = logging.getLogger(__name__)


class GameState:
    finished = True
    ongoing = False


class Board:
    columns = 7
    rows = 6
    shape = (rows, columns)
    empty = 0
    winning_sequence_length = 4

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

    def check_sequence(self, vector, seq_length=None):
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

    def check_if_not_full(self):
        for i in range(self.columns):
            if self.grid[0][i] == 0:
                return True
        log.debug(
            f"Grid is full, it is a draw"
        )
        return False

    def check_result_vertical(self):
        log.debug(f"VERTICAL CHECK")
        for col in range(self.columns):
            current_column_vec = self.grid[:, col]
            result = self.check_sequence(current_column_vec)
            if result != 0:
                return True
        return False

    def check_result_horizontal(self):
        log.debug(f"HORIZONTAL CHECK")
        for row in range(self.rows):
            current_row_vec = self.grid[row]
            result = self.check_sequence(current_row_vec)
            if result != 0:
                return True
        return False

    def check_result_diagonal(self):
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


class Game:
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
                if self.board.check_if_not_full():
                    self.switch_player()
                else:
                    self.game_state = GameState.finished
        else:
            return
    
    def move_player(self, column, current_player):
        self.current_player = current_player
        if self.board.drop_token(column, self.current_player):
            game_result = self.board.check_result()
            if game_result == GameState.finished:
                self.winner = self.current_player
                self.game_state = game_result
            else:
                if not self.board.check_if_not_full():
                    self.game_state = GameState.finished
        else:
            return


def main():
    bo = Board()
    log.debug(bo.grid)
    log.debug(bo.drop_token(3, 1))
    log.debug(bo.drop_token(3, 2))
    log.debug(bo.drop_token(3, 2))
    log.debug(bo.drop_token(3, 2))
    bo2 = Board()
    bo2.drop_token(1, 1)
    bo2.drop_token(2, 1)
    bo2.drop_token(3, 1)
    bo2.drop_token(4, 1)
    bo2.check_result()


if __name__ == "__main__":
    main()
