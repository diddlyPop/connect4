#################################################################################
#
# agents.py
#
# Player class is inherited by game players
#
# Human's choose their moves via the command line
#
# RandomAgent's choose their moves at random from the available moves
#
# IntelligentAgent's will use a neural network to predict the best next move
#
#################################################################################
import random


class Player:
    def __init__(self, number):
        """

        :param number: players token number, what they place on the board
        """
        self.number = number

    def choose_move(self, available, board_state):
        pass


class Human(Player):
    def choose_move(self, available, board_state):
        """
        Retrieves user input, verifies column number has an available space, and places that piece
        :param available:
        :param board_state:
        :return: none, but place pieces in board
        """

        print(f"Can place a piece at: {available}")
        choice = int(input("Column: "))
        while choice not in available:
            print("That column is full")
            choice = int(input("Column: "))
        return choice - 1


class RandomAgent(Player):
    def choose_move(self, available, board_state):
        return int(random.choice(available))-1


class IntelligentAgent(Player):
    def choose_move(self, available, board_state):
        pass
