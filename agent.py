import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

class Agent():
    def __init__(self):
        self.model = keras.Sequential()
        self.model.add(keras.Input(shape=(22,)))
        self.model.add(layers.Dense(64, activation='relu', input_shape=(22,)))
        self.model.add(layers.Dense(48, activation='relu'))
        self.model.add(layers.Dense(24, activation='relu'))
        self.model.add(layers.Dense(12, activation='relu'))
        self.model.add(layers.Dense(3, activation='relu'))
        print(self.model.summary())

