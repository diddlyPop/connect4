# main.py will control all three pipelines in alpha-zero
from agents import Human, RandomAgent, IntelligentAgent
from game import Connect4
from collections import deque
from model import NNet
import random

class NetController:
    def __init__(self):
        self.buffer_size = 10000
        self.buffer = deque(maxlen=self.buffer_size)
        self.batch_size = 512
        self.epochs = 5
        self.network = NNet()

    def start_pvp_game(self):
        player1 = Human(1)
        player2 = Human(2)
        game = Connect4(player1, player2, collection=False)
        winner, data = game.start()
        print(winner, data)

    def start_pve_game(self):
        player1 = Human(1)
        player2 = RandomAgent(2)
        game = Connect4(player1, player2, collection=False)
        winner, data = game.start()
        print(winner, data)

    def start_self_play(self, rounds=20):
        for _ in range(rounds):
            player1 = RandomAgent(1)
            player2 = RandomAgent(2)
            game = Connect4(player1, player2, collection=True)
            winner, data = game.start()
            print(winner, data)
            self.buffer.extend(data)

    def train_from_data(self):
        batch = random.sample(self.buffer, self.buffer_size)
        states_batch = [data[0] for data in batch]
        policies_batch = [data[1] for data in batch]
        winners_batch = [data[2] for data in batch]
        for _ in range(self.epochs):
            self.network.train_on_batch(states_batch, policies_batch, winners_batch)


if __name__ == '__main__':
    net = NetController()
    net.start_pve_game()

