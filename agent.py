from collections import deque
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras import Input
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import to_categorical
from consts import *
from vectors import *
import numpy as np

MAX_MEMORY = 100000

class Agent:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(64, activation='relu', input_dim=22))
        self.model.add(Dense(48, activation='relu'))
        self.model.add(Dense(24, activation='relu'))
        self.model.add(Dense(12, activation='relu'))
        self.model.add(Dense(3, activation='softmax'))

        self.model.compile(
            loss="mse",
            optimizer=Adam()
        )
        print(self.model.summary())

        self.memory = deque(maxlen=MAX_MEMORY)
    
    def get_action(self, state):
        pred = self.model.predict(state.reshape(1, 22))
        move = to_categorical(np.argmax(pred[0]), num_classes=3)
        clockwise_dir = [UP, RIGHT, DOWN, LEFT]
        cnt = 0
        
        if move[0] == 1.0:
            cnt -= 1
        elif move[2] == 1.0:
            cnt += 1
        
        if state[1] == 1:
            cnt += 2
        elif state[2] == 1:
            cnt += 1
        elif state[3] == 1:
            cnt += 3

        return clockwise_dir[cnt%4]
