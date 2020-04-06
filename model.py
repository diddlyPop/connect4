import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical


class NNet:
    def __init__(self):
        """
        input: 6x7 for board size, 2 layers per turn, 4 turns of history
        output: policy head and value head
        """
        self.model = Sequential([
            Dense(64, activation='relu', input_shape=(6, 7, 8)),
            Dense(64, activation='relu'),
            Dense(10, activation='softmax'),
        ])

    def train_on_batch(self, states_batch, probabilities_batch, winners_batch):
        pass

