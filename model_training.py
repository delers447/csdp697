
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D, BatchNormalization, Reshape
import time

np.set_printoptions(suppress=True)

def get_data():
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

        if i%10_000 == 0:
            print(i)
        if i == 100_000:
            break

    return np.array(x_train), np.array(y_train), np.array(x_test), np.array(y_test)

def reshape_test_data(test_data):
    data = []
    for line in test_data:
        data.append(np.reshape(line, (9,9)))
    #print(test_data[0])
    #print(data[0])
    return np.array(data)

def reshape_prob_to_matrix(probs):
    data = []
    for line in probs:
        #print(f"{line} is {np.argmax(line)+1}")
        data.append(np.argmax(line)+1)
    return data

def get_list_of_zeros(matrix):
    matrix = matrix.flatten()
    zeros = []
    for i in range(len(matrix)):
        if matrix[i]== 0:
            zeros.append(i)
    return zeros

def get_max_prob(x_test, predictions):
    max_prob, max_index, max_prediction = 0, 0, 0
    zeros = get_list_of_zeros(x_test)
    #print(f"zeros: {zeros}")
    for index in zeros:
        prob, cord  = np.max(predictions[index]), np.argmax(predictions[index])
        #print(f"zero: {index}, prob: {prob}, cord: {cord}")
        if prob > max_prob:
            #print(f"NEW MAX FOUND===> index: {index}, old_max: {max_prob}, prob: {prob}, cord: {cord}")
            #print(predictions[index])
            max_prob, max_index, max_prediction = prob, index, cord
    return max_prob, max_index, max_prediction+1

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

def get_model():
    model = Sequential()

    model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same', input_shape=(9,9,1)))
    model.add(BatchNormalization())
    model.add(Conv2D(64, kernel_size=(3,3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(Conv2D(128, kernel_size=(1,1), activation='relu', padding='same'))

    model.add(Flatten())
    model.add(Dense(81*9))
    model.add(Reshape((-1, 9)))
    model.add(Activation('softmax'))

    model.compile(loss='MSE', optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model

x_train, y_train, x_test, y_test = get_data()

model = get_model()
#model = tf.keras.models.load_model('might_be_awesome.model')
#model.summary()


#model.fit(reshape_test_data(y_train), y_train, batch_size=20, epochs=10)
model.fit(x_train, y_train, batch_size=20, epochs=2)
predictions = model.predict([x_test])


print("-"*10 + "Prediction" + "-"*10)
print(predictions[1].shape)
print(predictions[1])
max_prob, cord, prediction = get_max_prob(x_test[1], predictions[1])
print(f"cord: {cord}, prob:{max_prob}, prediction: {prediction}")

print("-"*10 + "Y_test" + "-"*10)
print(y_test[1].shape)
#print(y_test[1])
cord = np.argmax(y_test[1].flatten())
print(cord)
print(y_test[1].flatten()[cord])

correct, tries = 0, 0
x, y = [], []

for j in range(31, 81, 1):
    predictions = model.predict([x_test])
    temp_list = []
    for i in range(len(predictions)):

        max_prob, cord, prediction = get_max_prob(x_test[i], predictions[i])

        preidction_matrix = reshape_prob_to_matrix(predictions[i])
        solution_matrix = reshape_prob_to_matrix(y_test[i])

        print("-"*10 + str(f"{j}:{i}") + "-"*10)
        print(f"The best probability is {max_prob} which is at coordinate {cord}.")
        print(f"The solution spot is {solution_matrix[cord]} where the prediction is {preidction_matrix[cord]}.")
        temp_list.append(max_prob)
        if solution_matrix[cord] == preidction_matrix[cord]:
            print("===>They were the same!")
            correct += 1
        tries += 1

        x_temp = x_test[i]
        x_temp = x_temp.flatten()
        x_temp[cord] = preidction_matrix[cord]
        x_test[i] = np.reshape(x_temp, (9,9))
    x.append(j), y.append(np.average(temp_list))

print(f"The next best guess was correct {correct} out of {tries} times, which is {correct / tries * 100}%!")

print("-"*10 + "Seed" + "-"*10)
print(x_test[0])

print("-"*10 + "Prediction" + "-"*10)
print(np.reshape(reshape_prob_to_matrix(predictions[0]), (9, 9)))

print("-"*10 + "Solution" + "-"*10)
print(np.reshape(reshape_prob_to_matrix(y_test[0]), (9, 9)))

val_loss, val_acc = model.evaluate(x_test, y_test)
print(val_loss, val_acc)

#model.save("might_suck.model")

plt.plot(x, y)
plt.show()

'''
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

'''
