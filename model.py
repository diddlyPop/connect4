#################################################################################
#
# model.py
#
# NNet class will contain all keras functionality
#
# Network has input layer that reads in the boards 6x7 matrix
#
# The output layer has two heads:
#   Policy head for individual column probabilities
#   Value head for indicating when a loss or win is expected
#
# Trains on batches of data from self-play:
#   Batch consists of each turn's 'encoded state block',
#   probabilities from the policy head, and bool for if that player won the game
#
#################################################################################

import numpy as np
from keras.models import Sequential
from keras.layers import Dense
from keras.utils import to_categorical
from keras.models import *
from keras.layers import *
from keras.optimizers import *


class NNet:
    def __init__(self):
        """
        input: 6x7 for board size, 2 layers per turn, 4 turns of history
        output: policy head and value head
        """
        self.board_x = 6
        self.board_y = 7
        self.dropout = 0.3
        self.channels = 512
        self.cuda = True
        self.learning_rate = 0.01
        self.num_of_actions = 7
        self.trained = False
        self.batch_size = 64    # can also try 512
        self.epochs = 5

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))  # s: batch_size x board_x x board_y

        x_image = Reshape((self.board_x, self.board_y, 1))(self.input_boards)  # batch_size  x board_x x board_y x 1
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(self.channels, 3, padding='same')(
                x_image)))  # batch_size  x board_x x board_y x num_channels
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(self.channels, 3, padding='same')(
                h_conv1)))  # batch_size  x board_x x board_y x num_channels
        h_conv3 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(self.channels, 3, padding='same')(
                h_conv2)))  # batch_size  x (board_x-2) x (board_y-2) x num_channels
        h_conv4 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(self.channels, 3, padding='valid')(
                h_conv3)))  # batch_size  x (board_x-4) x (board_y-4) x num_channels
        h_conv4_flat = Flatten()(h_conv4)
        s_fc1 = Dropout(self.dropout)(Activation('relu')(
            BatchNormalization(axis=1)(Dense(1024)(h_conv4_flat))))  # batch_size x 1024
        s_fc2 = Dropout(self.dropout)(
            Activation('relu')(BatchNormalization(axis=1)(Dense(512)(s_fc1))))  # batch_size x 1024
        self.policy = Dense(self.num_of_actions, activation='softmax', name='policy')(s_fc2)  # batch_size x self.action_size
        self.value = Dense(1, activation='tanh', name='value')(s_fc2)  # batch_size x 1

        self.model = Model(inputs=self.input_boards, outputs=[self.policy, self.value])
        self.model.summary()
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate=self.learning_rate))


    def train_on_batch(self, states_batch, probabilities_batch, winners_batch):
        states_batch = np.asarray(states_batch)
        probabilities_batch = np.asarray(probabilities_batch).reshape((512, 7))
        winners_batch = np.asarray(winners_batch)
        self.model.fit(states_batch, [probabilities_batch, winners_batch], batch_size=self.batch_size, epochs=self.epochs)
