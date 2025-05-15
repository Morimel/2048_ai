import numpy as np
import random

class Game2048:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = np.zeros((4, 4), dtype=int)
        self.score = 0
        self.add_tile()
        self.add_tile()
        return self.get_state()

    def get_state(self):
        norm_board = tuple((np.log2(self.board + 1).astype(int)).flatten())
        return norm_board


    def add_tile(self):
        empty = list(zip(*np.where(self.board == 0)))
        if empty:
            x, y = random.choice(empty)
            self.board[x][y] = 2 if random.random() < 0.9 else 4

    def move(self, action):
        def merge(row):
            non_zero = row[row != 0]
            new_row = []
            skip = False
            for i in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if i+1 < len(non_zero) and non_zero[i] == non_zero[i+1]:
                    new_row.append(non_zero[i]*2)
                    self.score += non_zero[i]*2
                    skip = True
                else:
                    new_row.append(non_zero[i])
            return np.array(new_row + [0]*(4-len(new_row)))

        old_board = self.board.copy()
        for i in range(4):
            if action == 0:  # up
                self.board[:, i] = merge(self.board[:, i])
            elif action == 1:  # down
                self.board[:, i] = merge(self.board[::-1, i])[::-1]
            elif action == 2:  # left
                self.board[i] = merge(self.board[i])
            elif action == 3:  # right
                self.board[i] = merge(self.board[i][::-1])[::-1]

        if not np.array_equal(old_board, self.board):
            self.add_tile()
            reward = self.score
        else:
            reward = -5  # штраф за неэффективное действие

        done = not self.can_move()
        return self.get_state(), reward, done

    def can_move(self):
        if np.any(self.board == 0):
            return True
        for i in range(4):
            for j in range(4):
                if (i+1 < 4 and self.board[i][j] == self.board[i+1][j]) or \
                   (j+1 < 4 and self.board[i][j] == self.board[i][j+1]):
                    return True
        return False
