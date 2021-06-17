import copy
import random

import numpy


# p1 = 0
# p2 = 1


class Connect4:
    def __init__(self):
        self.turn = random.randint(0, 1)
        self.board = [[-1 for x in range(7)] for y in range(6)]

    def is_legal_move(self, c):
        if c < 0 or c > 6:
            return False
        if self.board[0][c] != -1:  # row can't be full
            return False
        if self.has_player_won():
            return False
        return True

    def move(self, column):
        if self.is_legal_move(column):
            for i in range(5, -1, -1):
                if self.board[i][column] == -1:
                    self.board[i][column] = self.turn
                    if not self.has_player_won() or self.is_board_full():
                        self.change_turn()
                    break

    def has_player_won(self):
        return self.has_four_vertical() or self.has_four_horizontal() or self.has_four_diagonal()

    def has_four_horizontal(self):
        for r in range(len(self.board)):
            counter = 0
            for c in range(len(self.board[r])):
                if self.board[r][c] == self.turn:
                    counter += 1
                else:
                    counter = 0
                if counter == 4:
                    return True
        return False

    def has_four_vertical(self):
        copy_board = copy.deepcopy(self.board)
        flipped_board = numpy.array(copy_board).transpose()
        for r in range(len(flipped_board)):
            counter = 0
            for c in range(len(flipped_board[r])):
                if flipped_board[r][c] == self.turn:
                    counter += 1
                else:
                    counter = 0
                if counter == 4:
                    return True
        return False

    def has_four_diagonal(self):
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                try:
                    counter = 0
                    for i in range(4):
                        if self.board[r + i][c + i] == self.turn:
                            counter += 1
                        else:
                            counter = 0
                        if counter == 4:
                            return True
                except IndexError:
                    pass
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                try:
                    counter = 0
                    for i in range(4):
                        if self.board[r + i][c - i] == self.turn:
                            counter += 1
                        else:
                            counter = 0
                        if counter == 4:
                            return True
                except IndexError:
                    pass
        return False

    def is_board_full(self):
        for c in self.board[0]:
            if c == -1:
                return False
        return True

    def change_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def get_board(self):
        return copy.deepcopy(self.board)
