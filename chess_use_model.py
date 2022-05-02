#import some modules
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Reshape
import time

model = tf.keras.models.load_model("chess_final.model")

def get_prob(game_data):
    """  Input the 8x8 grid as a 2D array and out putted is the probability matrix."""
    game_data = np.array( [game_data,] )
    predictions = model.predict([game_data])
    return predictions[0]

def example():
    """Here's an example for your Chib."""
    game_data = [[1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1],
                [0, 0, 1, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 1, 0, 0, 0, 0],
                [0, 1, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1, 0, 0, 0]]
    print(get_prob(game_data))