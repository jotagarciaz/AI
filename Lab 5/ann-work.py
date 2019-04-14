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
OUTPUT_LAYER=10
LEARNING_RATE=0.01

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

class Neuron:

    output=0
    net=0
    inputs=[]
    weights=[]
    def __init__(self):
        self.output=0
        self.net=0
        self.inputs=[]
        self.weights=[]

    def clear_variables(self):
        self.output=0
        self.net=0
        self.inputs=[]
    
    def add_weights(self,weight):
        self.weights.append(weight)

    def sum(self,inpt,weight):
        self.inputs.append(inpt)
        self.net=self.net+(inpt*weight)
    def sigmoid(self):
        self.output= 1/(1+math.exp(self.net))
    def sign(self):
        self.output= 1 if self.net>0 else -1
    def __repr__(self):
        return "output: %i" % (self.output)    
    def __str__(self):
        return "output: %i" % (self.output)   


""" First we need to extract values from the file"""
def read_training_set():
    n_lines_training = int(PERCENTAGE_TRAINING * n_lines_to_read)
    training_set = []  # type: list
    f.seek(0)
    for i in range(0, 1): #n_lines_training):
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
    #validation_set=read_validation_set()
    #testing_set=read_testing_set()

    return training_set#,validation_set,testing_set

def calculate_weight():
    return random.uniform(-1,1)

def initialize_hidden_layer():
    list_neurons_hidden_layer=[]
    for i in range (0,HIDDEN_LAYER_FIRST_LAYER):
        n = Neuron()    
        weight=calculate_weight() 
        n.add_weights(weight)
        n.sum(1,weight) #W0 
        list_neurons_hidden_layer.append(n)
    return list_neurons_hidden_layer


def initialize_output_layer():
    list_neurons_output_layer=[]
    for i in range (0,OUTPUT_LAYER):
        n = Neuron()            
        weight = calculate_weight()
        n.add_weights(weight)
        n.sum(1,weight) #W0 
        list_neurons_output_layer.append(n) 
    return list_neurons_output_layer

def calculate_softmax(list_neurons_output_layer):
    softmax=[]
    for no in list_neurons_output_layer:
        no.sigmoid() #¿Es necesario?
        softmax.append(no.output)

    softmax=list(map(lambda x: math.exp(x) ,softmax))
    softmax=list(map(lambda x: x/sum(softmax),softmax))
    output=softmax.index(max(softmax))
    return output

def err_output_layer(set,output_neurons):
    error_at_output_layer=[]
    for t in set:
        t[COLUMN_RESULT]
        target=[(1 if  i is t[COLUMN_RESULT] else 0) for i in range(OUTPUT_LAYER)]
        for idx,no in enumerate(output_neurons):
            error_at_output_layer.append((target[idx]-no.output)*no.output*(1-no.output))

    for idxno,no in enumerate(output_neurons):
        for idx,x in enumerate(no.inputs):
            no.weights[idx]+=LEARNING_RATE*error_at_output_layer[idxno]*x
    return error_at_output_layer

def err_hidden_layer(set,neurons_hidden,neurons_output,error_at_output_layer):
    error_at_hidden_layer=[]
    for t in set:
        for idx,nh in enumerate(neurons_hidden):
            suma=0
            for idxno, no in enumerate(neurons_output):
                suma+=error_at_output_layer[idxno]*no.weights[idxno]
            error_at_hidden_layer.append((1-nh.output)*(nh.output)*suma)

    for idxnh,nh in enumerate(neurons_hidden):
        for idx,x in enumerate(nh.inputs):
            nh.weights[idx]+=LEARNING_RATE*error_at_hidden_layer[idxnh]*x
    return error_at_hidden_layer

def clean_layers(list_neurons_hidden_layer,list_neurons_output_layer):
    for n in list_neurons_hidden_layer :
        n.clear_variables()
    for n in list_neurons_output_layer :
        n.clear_variables()


def main():
   #,validation_set,testing_set,
    
    training_set=read_all_sets()
    list_neurons_hidden_layer=initialize_hidden_layer()
    list_neurons_output_layer=initialize_output_layer()

    for i in range(1,LINE_LEN):
        for n in list_neurons_hidden_layer :
            weight=calculate_weight() 
            n.add_weights(weight)
    
    #Iniciamos
    for nh in list_neurons_hidden_layer:
        for no in list_neurons_output_layer:
            no.add_weights(calculate_weight())

    for t in training_set:
        for i in range(1,LINE_LEN):
            for n in list_neurons_hidden_layer :
                inpt=t[i]
                n.sum(inpt, n.weights[i])

    for nh in list_neurons_hidden_layer:
        nh.sign() #to do signal function maybe we should change and solve the problems of the sigmoid
        for no in list_neurons_output_layer:
            no.sum(nh.output,calculate_weight())
    
    
    output=calculate_softmax(list_neurons_output_layer)
    
    # Backpropagation

    print("Output: ", output)

    # Error Output Layer
    error_at_output_layer=err_output_layer(training_set,list_neurons_output_layer)
    
    #Error Hidden Layer
    err_hidden_layer(training_set,list_neurons_hidden_layer,list_neurons_output_layer,error_at_output_layer)

    clean_layers(list_neurons_hidden_layer,list_neurons_output_layer)

main()