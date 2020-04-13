#################################################################################
#
# main.py
#
# NetController class currently contains functionality for a few types of games
#
# PvP game is between two Humans on the same machine
#
# PvE game is between a Human and a RandomAgent
#
# Self-play is between two RandomAgents for 20 games
#
#################################################################################
from agents import Human, RandomAgent, IntelligentAgent
from game import Connect4
from collections import deque
import random
import time


class GameController:
    def __init__(self):
        self.buffer_size = 10000
        self.buffer = deque(maxlen=self.buffer_size)
        self.batch_size = 512
        self.epochs = 5
        # self.network = NNet()

    def start_pvp_game(self):
        player1 = Human(1)
        player2 = Human(2)
        game = Connect4(player1, player2, collection=False)
        winner, data = game.start()
        print(f"The winner was Player {winner}!")
        print(f"Data collected during match: {data}")

    def start_pve_game(self):
        player1 = Human(1)
        player2 = RandomAgent(2)
        game = Connect4(player1, player2, collection=False)
        winner, data = game.start()
        print(f"The winner was Player {winner}!")
        print(f"Data collected during match: {data}")

    def start_self_play(self, rounds=1000):
        self_play_winners = {1: 0, 2: 0, "DRAW": 0}
        player1 = RandomAgent(1)
        player2 = IntelligentAgent(2)
        now = time.time()
        for i in range(rounds):
            game = Connect4(player1, player2, collection=True)
            winner, data = game.start()
            self.buffer.extend(data)
            self_play_winners[winner] += 1
            if i % 100 == 0:
                self.train_from_data(player2)

        later = time.time()
        total = later - now
        print(f"Games won by Player 1: {self_play_winners[1]}!")
        print(f"Games won by Player 2: {self_play_winners[2]}!")
        print(f"Draws: {self_play_winners['DRAW']}!")
        print(f"Data collected during match: {data}")
        print(f"Time during {rounds} matches: {total:.2f}s")

    def train_from_data(self, player):
        batch = random.sample(self.buffer, self.batch_size)
        states_batch = [data[0] for data in batch]
        policies_batch = [data[1] for data in batch]
        winners_batch = [data[2] for data in batch]
        for _ in range(self.epochs):
            player.learn(states_batch, policies_batch, winners_batch)


if __name__ == '__main__':
    coach = GameController()
    coach.start_self_play()

