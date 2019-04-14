from copy import deepcopy 
import math
import random

f = open("training", 'r')
f.seek(0)
n_lines_to_read = len(f.readlines())
LINE_LEN=784
PERCENTAGE_TRAINING=0.7
PERCENTAGE_VALIDATION=0.2
PERCENTAGE_TEST=0.1
COLUMN_RESULT = 0
GROUPS = 7
N_ELEMENTS_BY_GROUP=28/GROUPS

HIDDEN_LAYER_FIRST_LAYER=20

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def read_training_set():
    n_lines_training = int(PERCENTAGE_TRAINING * n_lines_to_read)
    training_set = []  # type: list
    f.seek(0)
    for i in range(0, n_lines_training):
        aux = f.readline()
        training_set.append(aux.split(",", LINE_LEN))

    for i in range(0, len(training_set)):
        training_set[i] = list(map(lambda x: num(x), training_set[i]))

    return training_set

def read_validation_set():
    global f, n_lines_to_read
    n_lines_validation = int(PERCENTAGE_VALIDATION * n_lines_to_read)
    validation_set = []  # type: list
    for i in range(0, n_lines_validation):
        aux = f.readline()
        validation_set.append(aux.split(",", LINE_LEN))

    for i in range(0, len(validation_set)):
        validation_set[i] = list(map(lambda x: num(x), validation_set[i]))

    return validation_set

def read_testing_set():
    global f, n_lines_to_read
    n_lines_testing = int(PERCENTAGE_TEST * n_lines_to_read )
    testing_set = []  # type: list
    for i in range(0, n_lines_testing):
        aux = f.readline()
        testing_set.append(aux.split(",", LINE_LEN))

    for i in range(0, len(testing_set)):
        testing_set[i] = list(map(lambda x: num(x), testing_set[i]))

    return testing_set


def read_all_sets():
    training_set=read_training_set()
    validation_set=read_validation_set()
    testing_set=read_testing_set()

    return training_set,validation_set,testing_set


def calculate_weight():
    return random.uniform(-1,1)



def main():
   #training_set,validation_set,testing_set=read_all_sets()
   for i in range(1,GROUPS):
        for j in range(1,GROUPS):
            28 % 4 ==0


main()