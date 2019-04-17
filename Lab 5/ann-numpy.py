from copy import deepcopy 
import math
import random
import numpy as np

f = open("training", 'r')
f.seek(0)
n_lines_to_read = len(f.readlines())
LINE_LEN=785
PERCENTAGE_TRAINING=0.7
PERCENTAGE_VALIDATION=0.2
PERCENTAGE_TEST=0.1
COLUMN_RESULT = 0
SIZE_OUTPUT_LAYER=10
SIZE_FIRST_HIDDEN_LAYER=20


LEARNING_RATE=0.2

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
""" First we need to extract values from the file"""
def read_training_set():
    n_lines_training = int(PERCENTAGE_TRAINING * n_lines_to_read)
  
    f.seek(0)
    target=[]
    training_set=[]
    for i in range(0,3): #n_lines_training):
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=[]
        for i in range(1,len(aux)):
            line.append(num(aux[i])/255)
        
        training_set.append(line)
        target.append(aux[0])
             
    return training_set,target

def read_validation_set():
    global f, n_lines_to_read
    n_lines_validation = int(PERCENTAGE_VALIDATION * n_lines_to_read)
    validation_set = []  # type: list
    for i in range(0, n_lines_validation):
        aux = f.readline()
        validation_set.append(list(map(lambda x: num(x), aux.split(",", LINE_LEN))))

    return validation_set

def sigmoid(net):
  return  1/(1+np.exp(-net)) 

def main():

    input_layer_inputs = np.zeros(LINE_LEN-1)
    input_layer_weights=np.random.rand(LINE_LEN-1,SIZE_FIRST_HIDDEN_LAYER)
    input_layer_bias = np.random.rand(SIZE_FIRST_HIDDEN_LAYER)
    input_layer_output=0
    input_layer_net=0
    
    training_set,target=read_training_set()
    for t in training_set:
        for i in range(len(t)):
            input_layer_inputs[i]=t[i]

        input_layer_net=np.dot(input_layer_inputs,input_layer_weights)
        output = sigmoid(input_layer_net)
        print(output)
    
main()