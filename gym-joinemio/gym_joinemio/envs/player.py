import random

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
