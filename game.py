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
    def __init__(self, player1, player2, data_collection=False, print_boards=False, plot=True):
        """
        sets up player list, initializes game data, creates new board, and starts game
        """
        self.game_running = True
        self.players = [player1, player2]
        self.winner = None
        self.board = Board()
        self.data_collection = data_collection
        self.print_boards = print_boards
        self.plot = plot

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
                if self.print_boards:
                    self.board.print_board()
                # get column input from player
                results = player.choose_move(self.board.get_available_moves(), self.board.get_board_state_normal(player.number))
                choice, policy = results
                # place piece into board at this column
                self.board.place(choice, player.number)
                if self.data_collection:
                    # add turn to players turn history, augment perspective to show current player's pieces as 1
                    player.turns.append([self.board.get_board_state_normal(player.number), policy])
                # check if win conditions have been met
                if self.board.check_win(player.number):
                    # if a winner is found set this variable to contain the winners player number
                    self.game_running = False
                    number = player.number
                    self.winner = number
                    if self.print_boards:
                        self.board.print_board()
                    break
                # no win condition but check if there's still available moves
                elif not self.board.get_available_moves():
                    # game result was a draw
                    self.game_running = False
                    self.winner = "DRAW"
                    if self.print_boards:
                        self.board.print_board()
                    break

        # append extra dimension to players turn history with the result of if they won that game
        for player in self.players:
            if self.winner == player.number:
                player.add_winners(1)
            elif self.winner == "DRAW":
                player.add_winners(0)
            else:
                player.add_winners(-1)

        # game end print board
        if self.plot:
            self.board.plot_board()
            print(f"Game winning policy: {list([policy])}")
        # match history
        data = []

        # load each turn into list
        for i in range(len(self.players[0].turns)):
            data.append(self.players[0].turns[i])
            #if i < len(self.players[1].turns):
                #data.append(self.players[1].turns[i])

        # clear turn history
        for player in self.players:
            player.turns.clear()

        winner = self.winner

        return winner, data
