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

from keras.models import *
from keras.layers import *
from keras.optimizers import *


class NNet:
    def __init__(self):
        """
        input: 6x7 for board size
        output: policy head
        """
        self.board_x = 6
        self.board_y = 7
        self.dropout = 0.3
        self.cuda = True
        self.num_of_actions = 7
        self.batch_size = 64    # 64 or 512
        self.epochs = 5
        self.trained = False

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))

        x_image = Reshape((self.board_x, self.board_y, 1))(self.input_boards)
        conv_layer_1 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(512, 3, padding='same')(
                x_image)))
        conv_layer_2 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(512, 3, padding='same')(
                conv_layer_1)))
        conv_layer_3 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(512, 3, padding='same')(
                conv_layer_2)))
        conv_layer_4 = Activation('relu')(BatchNormalization(axis=3)(
            Conv2D(512, 3, padding='valid')(
                conv_layer_3)))
        flat_conv_layer_4 = Flatten()(conv_layer_4)
        drop_1 = Dropout(self.dropout)(Activation('relu')(
            BatchNormalization(axis=1)(Dense(1024)(flat_conv_layer_4))))
        drop_2 = Dropout(self.dropout)(
            Activation('relu')(BatchNormalization(axis=1)(Dense(512)(drop_1))))
        self.policy = Dense(self.num_of_actions, activation='softmax', name='policy')(drop_2)
        self.value = Dense(1, activation='tanh', name='value')(drop_2)

        self.model = Model(inputs=self.input_boards, outputs=[self.policy, self.value])
        # self.model.summary()
        self.model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate=0.01))

    def train_on_batch(self, states_batch, probabilities_batch, winners_batch):
        states_batch = np.array(states_batch)
        probabilities_batch = np.array(probabilities_batch)
        winners_batch = np.array(winners_batch)
        self.model.fit(states_batch, [probabilities_batch, winners_batch], batch_size=self.batch_size, epochs=self.epochs, verbose=0)
