import random
import torch
import torch.nn as nn


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


class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.net = nn.ModuleList([nn.Linear(6*7, 6*7) for i in range(3)])
        self.net.append(nn.Linear(6*7,7))

    def forward(self, input):
        x1 = torch.tensor(input.astype(float)).type(torch.FloatTensor)
        x = torch.flatten(x1)
        for layer in self.net:
            x = layer(x)
        return x.tolist()


class AIPlayer:
    @staticmethod
    def possible_moves(board_state):
        available_cols = []
        for i in range(len(board_state[0])):
            if board_state[0][i] == 0:
                available_cols.append(i)
        return available_cols

    def __init__(self):
        self.net = NeuralNetwork()

    def get_action(self, board_state):
        weigths =  self.net.forward(board_state)
        pos_nums = self.possible_moves(board_state)
        max_num = 0
        for col in pos_nums:
            if weigths[max_num] < weigths[int(col)]:
                max_num = int(col)
        return max_num
    
    def train(self, memory_buffer, batch_size):
        return 0
