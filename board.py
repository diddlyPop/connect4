import numpy as np


class Player:
    def __init__(self, number):
        self.number = number

    def choose_move(self, available):
        pass


class Human(Player):
    def choose_move(self, available):
        """
        Retrieves user input, verifies column number has an available space, and places that piece
        :param available:
        :return: none, but place pieces in board
        """

        print(f"Can place a piece at: {available}")
        choice = int(input("Column: "))
        while choice not in available:
            print("That column is full")
            choice = int(input("Column: "))
        return choice - 1


class Computer(Player):
    def choose_move(self, available):
        pass


class Board:
    def __init__(self):
        """
        initializes board to a zero'd out 6x7 matrix
        """
        # a 6x7 2d matrix
        self.matrix = np.zeros((6, 7), dtype=int)
        # a dictionary storing column numbers with the amount of pieces in that column
        self.cols = {0: 5, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5, 6: 5}

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


class Game:

    def __init__(self, player1, player2):
        """
        sets up player list, initializes game data, creates new board, and starts game
        """
        self.game_running = True
        self.players = [player1, player2]
        self.winner = None
        self.board = Board()
        self.start()

    def start(self):
        """
        main game loop
        :return: none, but displays winner at end of game
        """
        while self.game_running:
            for player in self.players:
                # display board
                self.board.print_board()
                # get column input from player
                choice = player.choose_move(self.board.get_available_moves())
                # place piece into board at this column
                self.board.place(choice, player.number)
                # check if win conditions have been met
                if self.board.check_win():
                    # if a winner is found set this variable to contain the winners player number
                    self.game_running = False
                    self.winner = player.number
                    break
        self.end()

    def end(self):
        print(f"Winner: {self.winner}")


if __name__ == '__main__':
    player1 = Human(1)
    player2 = Human(2)
    newGame = Game(player1, player2)

