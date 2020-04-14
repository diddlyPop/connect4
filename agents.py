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
        return choice - 1, [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7]


class RandomAgent(Player):
    def choose_move(self, available, board_state):
        return int(random.choice(available))-1, [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7]


class IntelligentAgent(Player):
    def __init__(self, number):
        self.network = NNet()
        self.trained = True
        super().__init__(number)

    def choose_move(self, available, board_state):
        if self.trained:
            results = self.network.model.predict([(np.asarray(board_state)).reshape((1, 7, 6))])
            policy_output, value = results
            # print(f"Policy: {policy_output}")
            # print(f"Value: {value}")
            policy = policy_output[0]
            choice = np.argmax(policy)
            return choice, policy
            #if choice in available:
            #    print(f"Policy: {policy}")
            #    print(f"Choice: {choice}")
            #    return choice, policy
            #else:
            #    print(f"Policy: {policy}")
            #    print(f"Choice: {choice}")
            #    return NotImplementedError
        else:
            choice = int(random.choice(available)) - 1
            return choice, [1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7, 1 / 7]

    def learn(self, states, policies, winners):
        self.network.train_on_batch(states, policies, winners)
        if self.trained is False:
            self.trained = True
            print("HAS BEEN TRAINED")
