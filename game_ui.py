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
from agents import GUIAgent, IntelligentAgent
import sys

RED = (255, 0, 0)
BLUE = (0,0,255)
class UI:
    def __init__(self, player1, player2):
        self.width = 720
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.runGame = True
        self.drawBoard = True
        self.players = [player2, player1]

        self.images = ['0', '1', '-1']
        self.IMAGES = {name: pygame.image.load('images/{}.png'.format(name)).convert_alpha()
          for name in self.images}

        self.squareHeight = 64
        self.squareWidth = 60
        self.boardYOffset = 50
        self.boardXOffset = 150

        self.turn = 1

        self.grid = [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ]
        self.winner = None
        self.board = Board()
        self.choice = None

    def mainLoop(self):
        results = self.players[1].choose_move(self.board.get_available_moves(),
                                      self.board.get_board_state_normal(self.players[1].number))
        choice, policy = results
        # place piece into board at this column
        self.board.place(choice, self.players[1].number)
        self.grid = self.board.get_board_state_normal(1)
        self.turn *= -1
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
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if (pos[1] >= (self.boardYOffset) and pos[1] <= (self.boardYOffset + (8 * self.squareHeight))
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
                            for player in self.players:
                                if player.number == -1:
                                    player.choice = col
                                results = player.choose_move(self.board.get_available_moves(),
                                                              self.board.get_board_state_normal(player.number))
                                choice, policy = results
                                print(policy)
                                # place piece into board at this column
                                self.board.place(choice, player.number)
                                player.turns.append([self.board.get_board_state_normal(player.number), policy])
                                if self.board.check_win(player.number):
                                    # if a winner is found set this variable to contain the winners player number
                                    self.runGame = False
                                    number = player.number
                                    self.winner = number
                                    if self.winner == -1:
                                        label = myfont.render(f"Human won the game!", player.number, RED)
                                        self.screen.blit(label, (40,500))
                                    else:
                                        label = myfont.render(f"Computer won the game!", player.number, BLUE)
                                        self.screen.blit(label, (40, 500))
                                    print(f"Player {self.winner} won the game")

                                # no win condition but check if there's still available moves
                                elif not self.board.get_available_moves():
                                    # game result was a draw
                                    self.runGame = False
                                    self.winner = "DRAW"
                                    label = myfont.render(f"DRAW", player.number, RED)
                                    self.screen.blit(label, (40, 500))
                                    print(self.winner)


                            self.grid = self.board.get_board_state_normal(1)
                            print(self.grid)
                            if self.drawBoard:
                                for row in range(6):
                                    for col in range(7):
                                        rect = self.IMAGES[str(self.grid[row][col])].get_rect(topleft=(
                                            (self.boardXOffset + (col * self.squareWidth)),
                                            (self.boardYOffset + (row * self.squareHeight))))
                                        self.screen.blit(self.IMAGES[str(self.grid[row][col])], rect)
                                        pygame.display.update()
                            pygame.time.wait(2)
                    if not self.runGame:
                        for player in self.players:
                            if self.winner == player.number:
                                player.add_winners(1)
                            elif self.winner == "DRAW":
                                player.add_winners(0)
                            else:
                                player.add_winners(-1)
                        turn_info = []

                        # load each turn into list
                        for i in range(len(self.players[1].turns)):
                            turn_info.append(self.players[1].turns[i])
                            if i < len(self.players[0].turns):
                                turn_info.append(self.players[0].turns[i])

                        states_batch = [data[0] for data in turn_info]
                        policies_batch = [data[1] for data in turn_info]
                        winners_batch = [data[2] for data in turn_info]
                        for _ in range(5):
                            self.players[1].learn(states_batch, policies_batch, winners_batch)
                        self.players[1].save_checkpoint()
                        pygame.time.wait(4000)




if __name__ == "__main__":
    pygame.init()
    '''logo = pygame.image.load("images/logo.png")
    pygame.display.set_icon(logo)'''
    pygame.display.set_caption("Connect Four!")
    frank = IntelligentAgent(1, trained=True)
    frank.load_checkpoint(filename='basic.pth.tar')
    human = GUIAgent(-1)
    project = UI(frank, human)
    myfont = pygame.font.SysFont("monospace", 48)
    project.mainLoop()

