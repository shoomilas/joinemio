import random
import torch
import torch.nn as nn


class RandomPlayer:
    
    @staticmethod
    def get_action(board_state):
        def possible_moves(board_state):
            available_cols = []
            for i in range(len(board_state[0])):
                if board_state[0][i] == 0:
                    available_cols.append(i)
            return available_cols
        
        moves_available = possible_moves(board_state)
        if len(moves_available) == 0: return None
        return random.choice(moves_available)