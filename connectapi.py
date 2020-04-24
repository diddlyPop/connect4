from flask import Flask
from agents import IntelligentWebAgent, WebAgent
from game import Connect4
import tensorflow as tf

import threading


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/newgame')
def new_game():
    game = Connect4(frank, human, print_boards=True)
    game.start()
    return "Game made"


@app.route('/choice')
def make_choice():
    choice = 1
    human.choice = choice
    return "Recorded choice"


@app.route('/board')
def get_board():
    print(game.board.get_board_state_normal(1))
    return "Printed board"


if __name__ == '__main__':
    frank = IntelligentWebAgent(1, trained=True)
    # frank.graph = tf.get_default_graph()
    human = WebAgent(-1)
    game = Connect4(frank, human, print_boards=True)
    t = threading.Thread(target=game.start)
    t.daemon = True
    t.start()
    app.run(debug=True, threaded=True, use_reloader=False)  # host='0.0.0.0' keyword to access on another machine

