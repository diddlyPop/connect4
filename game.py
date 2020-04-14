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
        win_flag = 1
        lose_flag = -1
        while self.game_running:
            for player in self.players:
                # display board
                if self.collection is False:
                    self.board.print_board()
                # get column input from player
                results = player.choose_move(self.board.get_available_moves(), self.board.get_board_state())
                choice, policy = results
                # place piece into board at this column
                self.board.place(choice, player.number)
                if self.collection:
                    # TODO: if player 1 then augment the board to look like its from player 2 pov? might help w/ training
                    player.turns.append([self.board.get_board_state(), list([policy])])
                # check if win conditions have been met
                if self.board.check_win(player.number):
                    # if a winner is found set this variable to contain the winners player number
                    self.game_running = False
                    self.winner = player.number
                    if self.collection is False:
                        self.board.print_board()
                    break
                elif not self.board.get_available_moves():
                    self.game_running = False
                    self.winner = "DRAW"
                    self.board.print_board()
                    break
        for player in self.players:
            if self.winner == player.number:
                player.add_winners(1)
            elif self.winner == "DRAW":
                player.add_winners(0)
            else:
                player.add_winners(-1)

        data = []
        for i in range(len(self.players[0].turns)):
            data.append(self.players[0].turns[i])
            if i < len(self.players[1].turns):
                data.append(self.players[1].turns[i])

        for player in self.players:
            player.turns.clear()

        return self.winner, data
