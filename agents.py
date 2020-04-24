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
from model import NNet
import numpy as np
import os
import tensorflow as tf

RANDOM_POLICY = [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7]


class Player:
    def __init__(self, number):
        """

        :param number: players token number, what they place on the board
        """
        self.number = number
        self.turns = []

    def choose_move(self, available, board_state):
        pass

    def learn(self, states, policies, winners):
        pass

    def add_winners(self, win):
        for turn in self.turns:
            turn += [win]


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
        return choice - 1, RANDOM_POLICY


class RandomAgent(Player):
    def choose_move(self, available, board_state):
        return int(random.choice(available))-1, [(1 / len(available)) if i in available else 0 for i in range(1, 8)]


class IntelligentAgent(Player):
    def __init__(self, number, trained=False):
        self.network = NNet()
        self.trained = trained
        super().__init__(number)

    def choose_move(self, available, board_state):
        # uses network prediction if training flag is true
        if self.network.trained:
            results = self.network.model.predict([(np.array(board_state)).reshape((1, 6, 7))])
            policy_output, value = results
            policy = policy_output[0]
            for item in np.argsort(policy)[::-1]:
                if item+1 in available:
                    choice = item
                    break
            return choice, [each if i+1 in available else 0 for i, each in enumerate(policy)]
        else:
            choice = int(random.choice(available)) - 1
            return choice, [(1 / len(available)) if i in available else 0 for i in range(1, 8)]

    def learn(self, states, policies, winners):
        self.network.train_on_batch(states, policies, winners)
        self.network.trained = True

    def save_checkpoint(self, folder='models', filename='basic.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Creating models folder.")
            os.mkdir(folder)
        else:
            print("Found valid model")
        self.network.model.save_weights(filepath)

    def load_checkpoint(self, folder='models', filename='basic.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            print("No model found")
        self.network.model.load_weights(filepath)
        self.network.trained = True


class GUIAgent(Player):
    def __init__(self, number):
        self.choice = None
        super().__init__(number)

    def choose_move(self, available, board_state):
        while self.choice is None:
            pass
        choice_to_return = self.choice
        self.choice = None
        return choice_to_return, [(1 / len(available)) if i in available else 0 for i in range(1, 8)]

