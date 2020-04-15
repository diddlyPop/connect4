#################################################################################
#
# board.py
#
# Board class holds board rules, board data
#
# Methods available for placing pieces and checking if the game has been won
#
# All game handling is handled in game.py
#
#################################################################################
import numpy as np


class Board:
    def __init__(self):
        """
        initializes board to a zero'd out 6x7 matrix
        'cache' holds the last four previous turns
        """
        # a 6x7 2d matrix
        self.matrix = np.zeros((6, 7), dtype=int)
        # a dictionary storing column numbers with the amount of pieces in that column
        self.cols = {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}
        self.cache = []
        self.last_to_move = None
        self.NUM_COLS = 7
        self.NUM_ROWS = 6

    def get_board_state_player2_perspective(self, player_num):
        """"
        TODO: will encode board state to a format readable by our neural network
        TODO: will append the board states to the board cache
        """
        current_state = np.array(self.matrix)
        print(current_state)
        if player_num == 1:
            current_state[current_state == 1] = 3
            current_state[current_state == 2] = 1
            current_state[current_state == 3] = 2
            print("AUGMENTING")
            print(current_state)

        # self.cache.append(current_state)
        # encoded_state_block = self.cache
        # TODO: add logic here for creating the current encoded state block
        # encoded_state_block is 6x7x8 (6x7 for board size, 2 layers for each turn, 4 turns total of history)
        return current_state

    def get_board_state_normal(self):
        """"
        TODO: will encode board state to a format readable by our neural network
        TODO: will append the board states to the board cache
        """
        states = self.matrix

        return states

    def get_available_moves(self):
        """
        checks to see which columns are full and returns a list of available columns
        :return: 'available' list of columns
        """
        available = []
        for key in self.cols:
            if self.cols[key] >= 0:
                available.append(key+1)
        return available

    def check_win(self, players_number):
        """
        checks for win in all directions (diags, horiz, vert)
        check if array exists within a matrix
        a winning array for either play consists of their player number repeated four times
        if [1, 1, 1, 1] is found then player 1 wins
        if [2, 2, 2, 2] is found then player 2 wins
        :return: bool if game has been won
        """
        # diag
        for col in range(self.NUM_COLS - 3):
            for row in range(self.NUM_ROWS - 3):
                if self.matrix[row][col] == players_number \
                        and self.matrix[row + 1][col + 1] == players_number \
                        and self.matrix[row + 2][col + 2] == players_number \
                        and self.matrix[row + 3][col + 3] == players_number:
                    return True

        # diag
        for col in range(self.NUM_COLS - 3):
            for row in range(3, self.NUM_ROWS):
                if self.matrix[row][col] == players_number \
                        and self.matrix[row - 1][col + 1] == players_number \
                        and self.matrix[row - 2][col + 2] == players_number \
                        and self.matrix[row - 3][col + 3] == players_number:
                    return True
        # vertical
        for col in range(self.NUM_COLS - 3):
            for row in range(self.NUM_ROWS):
                if self.matrix[row][col] == players_number \
                        and self.matrix[row][col + 1] == players_number \
                        and self.matrix[row][col + 2] == players_number \
                        and self.matrix[row][col + 3] == players_number:
                    return True

        # horizontal
        for col in range(self.NUM_COLS):
            for row in range(self.NUM_ROWS - 3):
                if self.matrix[row][col] == players_number \
                        and self.matrix[row + 1][col] == players_number \
                        and self.matrix[row + 2][col] == players_number \
                        and self.matrix[row + 3][col] == players_number:
                    return True

    def place(self, column, player):
        """
        places the player number into the board at a column
        :param column: which column to place a piece into the board matrix
        :param player: the player number that we insert into the matrix
        :return: maybe nothing
        """
        if self.cols.get(column) >= 0:
            row = self.cols.get(column)
            self.cols[column] -= 1
            self.matrix[row][column] = player
            self.last_to_move = player

    def reset_board(self):
        """
        just resets the entire board to 0
        :return: maybe nothing
        """
        self.matrix.fill(0)

    def print_board(self):
        """
        outputs board to console
        :return: none
        """
        print("")
        print("_________________________")
        print("1   2   3   4   5   6   7")
        print("-------------------------")
        output = '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.matrix])
        print(output)
        print("_________________________")
