import numpy as np


class Board:
    def __init__(self):
        """
        initializes board to a zero'd out 6x7 matrix
        """
        self.matrix = np.zeros((6, 7), dtype=int)
        self.cols = {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}

    def check_win(self):
        """
        checks for win in all directions (diags, horiz, vert)
        check if array exists within a matrix
        a winning array for either play consists of their player number repeated four times
        if [1, 1, 1, 1] is found then player 1 wins
        if [2, 2, 2, 2] is found then player 2 wins
        :return: bool if game has been won
        """
        # TODO: add check win for game board
        pass

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


    def reset_board(self):
        """
        just resets the entire board to 0
        :return: maybe nothing
        """
        self.matrix.fill(0)

    def print_board(self):
        print("")
        print("_________________________")
        print("1   2   3   4   5   6   7")
        print("-------------------------")
        output = '\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.matrix])
        print(output)
        print("_________________________")


class Game:

    def __init__(self):
        self.game_running = True
        self.players = [1, 2]
        self.winner = None
        self.board = Board()
        self.start()

    def play_turn(self, player):
        self.board.print_board()
        choice = int(input("Column: ")) - 1
        self.board.place(choice, player)

    def start(self):
        while self.game_running:
            for player in self.players:
                self.play_turn(player)
                if self.board.check_win():
                    self.winner = player
                    break
        self.end()

    def end(self):
        print(f"Winner: {self.winner}")


if __name__ == '__main__':
    newGame = Game()
