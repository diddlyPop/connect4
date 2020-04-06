# main.py will control all three pipelines in alpha-zero
from agents import Human, RandomAgent, IntelligentAgent
from game import Connect4

if __name__ == '__main__':
    player1 = Human(1)
    player2 = RandomAgent(2)
    game = Connect4(player1, player2)
    game.start()
