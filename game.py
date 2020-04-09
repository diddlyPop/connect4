#################################################################################
#
# game.py
#
# Connect4 class runs the game and stores game-related information
#
# Human's choose their moves via the command line
#
# Mostly to abstract game loop out of Board class, but they could be combined
#
#################################################################################
from board import Board


class Connect4:
    def __init__(self, player1, player2, collection=False):
        """
        sets up player list, initializes game data, creates new board, and starts game
        """
        self.game_running = True
        self.players = [player1, player2]
        self.winner = None
        self.board = Board()
        self.collection = collection

    def start(self):
        """
        main game loop
        TODO: log state data
        :return: none, but displays winner at end of game
        """
        data = ""
        while self.game_running:
            for player in self.players:
                # display board
                self.board.print_board()
                # get column input from player
                choice = player.choose_move(self.board.get_available_moves(), self.board.get_board_state())
                # place piece into board at this column
                self.board.place(choice, player.number)
                # check if win conditions have been met
                if self.board.check_win(player.number):
                    # if a winner is found set this variable to contain the winners player number
                    self.game_running = False
                    self.winner = player.number
                    self.board.print_board()
                    break
                elif not self.board.get_available_moves():
                    self.game_running = False
                    self.winner = "DRAW"
                    self.board.print_board()
                    break
        return self.winner, data