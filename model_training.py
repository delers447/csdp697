
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization

np.set_printoptions(suppress=True)

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

        if i%1000 == 0:
            x_test.append(x)
            y_test.append(y)
        else:
            x_train.append(x)
            y_train.append(y)

        if i%10_000 == 0:
            print(i)

    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def reshape_test_data(test_data):
    data = []
    for line in test_data:
        data.append(np.reshape(line, (9,9)))
    print(test_data[0])
    print(data[0])
    return np.array(data)

def get_new2_model():
    model = Sequential()

    model.add(Flatten(input_shape=(9, 9, 1)))
    #model.add(Dense(81*3, activation=tf.nn.relu))
    model.add(Dense(81*2, activation=tf.nn.relu))
    model.add(Dense(81*2, activation=tf.nn.relu))
    model.add(Dense(81))

    model.compile(optimizer='adam', loss='MSE', metrics=['accuracy'])
    model.summary()
    return model

def get_new_model():
    model = Sequential()

    model.add(Conv2D(64, (3,3), padding='same', activation='relu', input_shape=(9, 9, 1)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

    model.add(Flatten())
    model.add(Dense(81*2, activation=tf.nn.relu))
    model.add(Dense(81))

    model.compile(optimizer='adam', loss='MSE', metrics=['accuracy'])
    model.summary()
    return model

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
#model.fit(reshape_test_data(y_train), y_train, batch_size=20, epochs=10)
model.fit(x_train, y_train, batch_size=20, epochs=10)
predictions = model.predict([x_test])
print(predictions[0])
model.save("might_suck.model")

print("-"*10 + "Seed" + "-"*10)
print(x_test[0])

print("-"*10 + "Actual" + "-"*10)
print(np.reshape(y_test[0], (9, 9)))

print("-"*10 + "Prediction" + "-"*10)
print(np.reshape(predictions[0], (9, 9)))

print("-"*10 + "Rounded Prediction" + "-"*10)
print(np.reshape(predictions[0].round(), (9, 9)).astype(int))

print("-"*10 + "Residual" + "-"*10)
print( np.reshape(y_test[0] - predictions[0], (9,9)))

#the idea:
#step 1: find the single index with the value clostest to an integer.
correct = 0
for i in range(len(predictions)):
    #print(f"The subtraction is {predictions[i]-predictions[i].round()}")
    differences =np.absolute(predictions[i]-predictions[i].round())
    cords = np.argmin(differences)
    print(f"The cords of the argmin is {cords} which was {differences[cords]}")
    print(f"The value is:{predictions[i][cords]}")
    print(f"The predicted value is:{predictions[i][cords].round()}")
    print(f"The correct value is: {y_test[i][cords]}")
    print("-"*10 + str(i) + "-"*10)

    if y_test[i][cords] == predictions[i][cords].round():
        correct += 1

print(f"The percent correct was {correct / len(predictions)}")

#step 2: add integer to the puzzle

#re-predict
#repeat steps 1-2 until puzzle filled.
val_loss, val_acc = model.evaluate(x_test, y_test)
print(val_loss, val_acc)
