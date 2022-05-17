
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
import random

def get_data():
    ''' internal function not used by Joey'''
    x_train = []
    y_train = []

    x_test = []
    y_test = []

    y_dict = {
            "1":[1, 0, 0, 0, 0, 0, 0, 0, 0],
            "2":[0, 1, 0, 0, 0, 0, 0, 0, 0],
            "3":[0, 0, 1, 0, 0, 0, 0, 0, 0],
            "4":[0, 0, 0, 1, 0, 0, 0, 0, 0],
            "5":[0, 0, 0, 0, 1, 0, 0, 0, 0],
            "6":[0, 0, 0, 0, 0, 1, 0, 0, 0],
            "7":[0, 0, 0, 0, 0, 0, 1, 0, 0],
            "8":[0, 0, 0, 0, 0, 0, 0, 1, 0],
            "9":[0, 0, 0, 0, 0, 0, 0, 0, 1],
            }

    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()):
        quiz, solution = line.split(',')

        if i == 0:
            continue

        x = []
        y = []

        for letter in quiz:
            x.append(int(letter))
        for letter in solution:
            y.append(y_dict[letter])

        x = np.reshape(x, (9, 9))

        if i%500 == 0:
            x_test.append(x)
            y_test.append(y)
        else:
            x_train.append(x)
            y_train.append(y)

        if i > 10_200:
            break

    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

x_train, y_train, x_test, y_test = get_data()
model = tf.keras.models.load_model('might_be_awesome.model')
#model.summary()

def get_list_of_zeros(matrix):
    '''internal function not used by Joey'''
    matrix = matrix.flatten()
    zeros = []
    for i in range(len(matrix)):
        if matrix[i]== 0:
            zeros.append(i)
    return zeros

def get_top_3(game_data):
    '''
    input the 9x9 board,
    output the top 3 measures as 3 tuples
    (p1, i1, y1), (p2, i2, y2), (p3, i3, y3)
    p is the probability, 1 is top, 2 is second, 3 is third highest
    i is index, 0-80.
    y is # guessed.
    ie:  (.98, 13, 2), (.96, 10, 9), (.72, 70, 3)
    top guess is 98% likely that in 13th spot is a 2
    second top guess is 96% likely that in 10th spot is a 9
    third top guess is 72% likely that in 70th spot is a 3
    '''
    game_data = np.array( [game_data,] )
    #print("one")
    predictions = model.predict([game_data])
    #print(predictions[0])
    predictions = predictions[0]
    max_prob, max_index, max_prediction = 0, 0, 0
    second_prob, second_index, second_prediction = 0, 0, 0
    third_prob, third_index, third_prediction = 0, 0, 0
    zeros = get_list_of_zeros(game_data)
    #print(f"zeros: {zeros}")
    for index in zeros:
        prob, cord  = np.max(predictions[index]), np.argmax(predictions[index])
        #print(f"zero: {index}, prob: {prob}, cord: {cord}")
        if prob > max_prob:
            #print(f"NEW MAX FOUND===> index: {index}, old_max: {max_prob}, prob: {prob}, cord: {cord}")
            #print(predictions[index])
            third_prob, third_index, third_prediction = second_prob, second_index, second_prediction
            second_prob, second_index, second_prediction = max_prob, max_index, max_prediction
            max_prob, max_index, max_prediction = prob, index, cord
    return (max_prob, max_index, max_prediction+1), (second_prob, second_index, second_prediction), (third_prob, third_index, third_prediction)

def from_nparray_into_python_array(np_array):
    p_array = [[0 for i in range(9)] for i in range(9)]
    for x in range(9):
        for y in range(9):
            p_array[x][y] = np_array[x][y]
    return p_array

def get_seed(number=False):
    ''' returns a 9x9 seed of 31 numbers
    given an index is optional, 1-10_000
    making consistent testing possible'''
    if number:

        return from_nparray_into_python_array(x_train[number])
    else:
        return from_nparray_into_python_array(x_train[random.randint(0,10_000)])

def example_for_foe():
    ''' example for joey'''
    print("Made it to the end!")
    print('-'*10 + "x_test[0]" + '-'*10)
    print(x_test[0])
    print('-'*10 + "Top three guesses" + '-'*10)

    #predictions = model.predict([x_test])
    #print(predictions[0])
    print(get_top_3(x_test[0]))
