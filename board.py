import numpy as np


class Board:
    def __init__(self):
        """
        initializes board to a zero'd out 6x7 matrix
        """
        self.matrix = np.zeros((6, 7), dtype=int)

    def check_win(self):
        """
        checks for win in all directions (diags, horiz, vert)
        check if array exists within a matrix
        a winning array for either play consists of their player number repeated four times
        if [1, 1, 1, 1] is found then player 1 wins
        if [2, 2, 2, 2] is found then player 2 wins
        :return: bool if game has been won
        """
        pass

    def place(self, column, player):
        """
        places the player number into the board at a column
        :param column: which column to place a piece into the board matrix
        :param player: the player number that we insert into the matrix
        :return: maybe nothing
        """
        pass

    def reset_board(self):
        """
        just resets the entire board to 0
        :return: maybe nothing
        """
        self.matrix.fill(0)


if __name__ == '__main__':
    newGame = Board()
