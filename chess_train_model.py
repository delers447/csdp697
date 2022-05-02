
#import some modules
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Reshape
import time

np.set_printoptions(suppress=True)

#import queens_problem_data_abridged as queens_problem_data
import queens_problem_data
print("hello world")

def get_y(data):
    
    temp_data = []
    for counter, datum in enumerate(data):
        temp_list = [[ 'a' for _ in range(8)] for __ in range(8)]
        temp_probs = []
        for x in range(8):
            for y in range(8):
                if datum[x][y] == 1:
                    temp_probs.append([1, 0])
                elif datum[x][y] == 0:
                    temp_probs.append([0, 1])
                else:
                    print(f"We got a typo:{datum[x][y]}, {counter}, {x}, {y}")
        #print(f"{counter}: {temp_probs}")
        temp_data.append(np.array(temp_probs))
    return temp_data

def get_model():
    model = Sequential()

    model.add(Flatten(input_shape=(8, 8)))

    model.add(Dense(1600))
    model.add(Activation('sigmoid'))

    model.add(Dense(800))
    model.add(Activation('sigmoid'))

    model.add(Dense(64*2))
    model.add(Reshape((-1, 2)))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()

    return model


x_data = queens_problem_data.get_data()
y_data = get_y(x_data)
x_data, y_data = np.array(x_data), np.array(y_data)

print(x_data[0])
print(y_data[0])

print(type(x_data[0]))
print(type(y_data[0]))

our_model = get_model()
our_model.fit(x_data, y_data, epochs=10_000)
our_model.save("chess_final.model")
predictions = our_model.predict([x_data])
print("=="*10 + "Preidction" + "=="*10)
print(predictions[0])
