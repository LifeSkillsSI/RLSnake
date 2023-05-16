from collections import deque
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential, load_model
from keras import Input
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import to_categorical
from consts import *
from vectors import *
import numpy as np
import random

MAX_MEMORY = 100000

class Agent:
    def __init__(self):
        self.model = Sequential()
        self.model.add(Dense(64, activation='relu', input_dim=22))
        self.model.add(Dense(48, activation='relu'))
        #self.model.add(Dense(24, activation='relu'))
        #self.model.add(Dense(12, activation='relu'))
        #self.model.add(Dense(3, activation='softmax'))

        #self.model.add(Dense(256, activation="relu", input_dim=22))
        self.model.add(Dense(3, activation="softmax"))

        self.model.compile(
            loss="mse",
            optimizer=Adam()
        )

        self.memory = deque(maxlen=MAX_MEMORY)
        self.gamma = 0.9
        self.game_count = 0
    
    def get_action(self, state):
        pred = self.model.predict(state, verbose = "0")
        move = to_categorical(np.argmax(pred[0]), num_classes=3)

        clockwise_dir = [UP, RIGHT, DOWN, LEFT]
        cnt = 0

        cnt += np.random.choice(
            a=[-1,0,1],
            size=1,
            p=move
        )[0]
        
        if state[0][1] == 1:
            cnt += 2
        elif state[0][2] == 1:
            cnt += 1
        elif state[0][3] == 1:
            cnt += 3

        return (clockwise_dir[cnt%4], pred)

    def train_short_memory(self, state, action, reward, new_state, alright):
        cur_gamma = self.gamma
        if not alright:
            target = reward
        else:
            
            target = reward + self.gamma * np.amax(self.model.predict(new_state, verbose = "0")[0])
        (_, target_f) = self.get_action(state)
        target_f[0][np.argmax(action)] = target
        self.model.fit(state, target_f, epochs = 1)
    
    def replay_mem(self, replay_batch_size):
        print("Replaying memory of game no", self.game_count)
        self.game_count += 1
        replay_batch_size = min(replay_batch_size, len(self.memory))
        batch = random.sample(self.memory, replay_batch_size)
        for (state, action, reward, new_state, alright) in batch:
            self.train_short_memory(state, action, reward, new_state, alright)

    def load_model(self, model_path):
        self.model = load_model(model_path)
        self.game_count = int(model_path.split('/')[-1])

