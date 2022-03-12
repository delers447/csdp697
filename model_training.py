
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D

def get_data():
    x_train = []
    y_train = []

    x_test = []
    y_test = []

    for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()):
        quiz, solution = line.split(',')

        if i == 0:
            continue

        x = []
        y = []

        for letter in quiz:
            x.append(int(letter))
        for letter in solution:
            y.append(int(letter))

        x = np.reshape(x, (9, 9))
        #y = np.reshape(y, ( 9, 9))

        if i%1000 == 0:
            x_test.append(x)
            y_test.append(y)
        else:
            x_train.append(x)
            y_train.append(y)

        print(i)
        #if i == 100_000:
        #    break

    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def get_model():
    model = Sequential()

    model.add(Conv2D(64, (3,3), padding='same', input_shape=(9, 9, 1)))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Conv2D(64, (3,3), padding='same'))
    model.add(Activation("relu"))
    model.add(MaxPooling2D(pool_size=(2,2)))

    model.add(Flatten())#input_shape=(9, 9, 1)))
    model.add(Dense(256, activation=tf.nn.relu))
    model.add(Dense(128, activation=tf.nn.relu))
    model.add(Dense(81))

    model.compile(optimizer='adam', loss='MSE', metrics=['accuracy'])
    model.summary()
    return model

x_train, y_train, x_test, y_test = get_data()
#x_train = tf.keras.utils.normalize(x_train, axis=1)
#x_test = tf.keras.utils.normalize(x_test, axis=1)
model = get_model()
model.fit(x_train, y_train, batch_size=20, epochs=5)
predictions = model.predict([x_test])
model.save("might_suck.model")

print("-"*10 + "Seed" + "-"*10)
print(x_test[0])
print("-"*10 + "Actual" + "-"*10)
print(np.reshape(y_test[0], (9, 9)))
#print("-"*10 + "Prediction-source" + "-"*10)
#print(np.reshape(predictions[0], (9, 9)))
print("-"*10 + "Prediction" + "-"*10)
print(np.reshape(predictions[0].round(), (9, 9)).astype(int))
#print("-"*10 + "Difference" + "-"*10)
#print(np.reshape(predictions[0].round(), (9, 9)).astype(int)-np.reshape(y_test[0], (9, 9)))
