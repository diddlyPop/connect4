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
import pygame
from pygame import image
from agents import GUIAgent, IntelligentWebAgent
import threading


class UI:
    def __init__(self):
        self.width = 600
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.runGame = True
        self.drawBoard = True

        self.images = ['0', '1', '-1']
        self.IMAGES = {name: pygame.image.load('images/{}.png'.format(name)).convert_alpha()
          for name in self.images}

        self.squareHeight = 64
        self.squareWidth = 60
        self.boardYOffset = 50
        self.boardXOffset = 50

        self.turn = 1

        self.grid = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, -1, 0, 0],
            [0, 0, 0, 1, -1, 1, 0]
        ]

    def mainLoop(self):
        global gui_choice
        #player1 = IntelligentWebAgent(1)
        #player2 = GUIAgent(-1)
        #game = Connect4(player1, player2)
        #game.start()
        while self.runGame:
            #recieve API call for board info - update grid
            if self.drawBoard:
                for row in range(6):
                    for col in range(7):
                        rect = self.IMAGES[str(self.grid[row][col])].get_rect(topleft=((self.boardXOffset + (col * self.squareWidth)),(self.boardYOffset + (row * self.squareHeight))))
                        self.screen.blit(self.IMAGES[str(self.grid[row][col])], rect)
                        pygame.display.update()
                #self.drawBoard = False
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if (pos[1] >= (self.boardYOffset) and pos[1] <= (self.boardYOffset + (8 * self.squareHeight)) #ensures action only occurs if they click inside the game board
                        and pos[0] >= self.boardXOffset and pos[0] <= (self.boardXOffset + (7 * self.squareWidth))):
                        col = (pos[0] - self.boardXOffset) // self.squareWidth
                        validMove = False
                        correctRow = 5
                        for row in range(6):
                            if self.grid[row][col] == 0:
                                validMove = True
                                correctRow = row
                        if validMove:
                            #send updated array to AI
                            #self.grid[correctRow][col] = gui_choice
                            gui_choice = col
                            self.turn *= -1


class Connect4:
    def __init__(self, player1, player2, data_collection=False, print_boards=False, plot=False):
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
        self.UI = UI()
        t = threading.Thread(target=self.start)
        t.daemon = True
        t.start()

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


if __name__ == "__main__":
    pygame.init()
    '''logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)'''
    pygame.display.set_caption("Connect Four!")
    frank = IntelligentWebAgent(1, trained=True)
    # frank.graph = tf.get_default_graph()
    human = GUIAgent(-1)
    project = Connect4(frank, human, print_boards=True)
    project.start()
