import numpy as np


class TetrisSim:
    def __init__(self, board_height=20):
        self.board_height = board_height
        self.board = None

    def board_init(self, board_arr):
        self.board = np.concatenate((np.zeros((self.board_height - board_arr.shape[0], 10), int) - 1, board_arr)) \
            if self.board_height > board_arr.shape[0] else board_arr[-self.board_height:, :]

    def can_fit_piece(self, piece, col, rot):
        board = np.concatenate((np.zeros((4, 10), int) - 1, self.board))
        pass
