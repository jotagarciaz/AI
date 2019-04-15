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
OUTPUT_LAYER=10

#NUMBER_OF_HIDDEN_LAYER=10
#HIDDEN_LAYER=150
#LEARNING_RATE=0.25

#NUMBER_OF_HIDDEN_LAYER=10
#HIDDEN_LAYER=100
#LEARNING_RATE=0.1

#NUMBER_OF_HIDDEN_LAYER=11
#HIDDEN_LAYER=110
#LEARNING_RATE=0.2

NUMBER_OF_HIDDEN_LAYER=2
NUMBER_OF_NODES_SMALLEST_LAYER=50
HIDDEN_LAYER=NUMBER_OF_HIDDEN_LAYER*NUMBER_OF_NODES_SMALLEST_LAYER

LEARNING_RATE=0.2

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)

class Neuron:

    output=0
    net=0
    inputs=np.array()
    weights=np.array()
    def __init__(self):
        self.output=0
        self.net=0
        self.inputs=np.array()
        self.weights=np.array()

    def clear_variables(self):
        self.output=0
        self.net=0
        self.inputs=np.array()
    
    def set_weights(self,weights):
        np.append(self.weights,weights)
    
    def add_weights(self,weight):
        np.append(self.weights,weight)

    def sum(self,inpt,weight):
        np.append(self.inputs,inpt)
        self.net=self.net+(inpt*weight)
    def sigmoid(self):
        self.output= 1/(1+math.exp(-self.net)) if self.net>=0  else math.exp(self.net)/(1+math.exp(self.net))
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
    for i in range(0,n_lines_training): #n_lines_training):
        aux = f.readline()
        image=list(map(lambda x: num(x)/255, aux.split(",", LINE_LEN)))
        image[0]=int(image[0]*255)
        training_set.append(image)
        
    return training_set

def read_validation_set():
    global f, n_lines_to_read
    n_lines_validation = int(PERCENTAGE_VALIDATION * n_lines_to_read)
    validation_set = []  # type: list
    for i in range(0, n_lines_validation):
        aux = f.readline()
        validation_set.append(list(map(lambda x: num(x), aux.split(",", LINE_LEN))))

    return validation_set

def read_testing_set():
    global f, n_lines_to_read
    n_lines_testing = int(PERCENTAGE_TEST * n_lines_to_read )
    testing_set = []  # type: list
    for i in range(0, n_lines_testing):
        aux = f.readline()
        testing_set.append(list(map(lambda x: num(x), aux.split(",", LINE_LEN))))

    return testing_set


def read_all_sets():
    training_set=read_training_set()
    validation_set=read_validation_set()
    testing_set=read_testing_set()

    return training_set, validation_set,testing_set

def calculate_weight():
    
    return random.uniform(-1,1)

def initialize_hidden_layer():
    list_neurons_hidden_layer=np.array()
    for j in range(0,NUMBER_OF_HIDDEN_LAYER):
        aux=np.array()
        for i in range (0,(j+1)*NUMBER_OF_NODES_SMALLEST_LAYER):
            n = Neuron()    
            weight=calculate_weight() 
            n.add_weights(weight)
            n.sum(1,weight) #W0 
            np.append(aux,n)
        np.append(list_neurons_hidden_layer,aux)
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
        softmax.append(math.exp(no.output))

    suma=sum(softmax)
    softmax=list(map(lambda x: x/suma,softmax))
    output=softmax.index(max(softmax))
    return output

def err_output_layer(t,output_neurons):
    error_at_output_layer=[]
    total_targets=[[(1 if i is  j else 0) for i in range(OUTPUT_LAYER)] for j in range(OUTPUT_LAYER)]
    target=total_targets[t[COLUMN_RESULT]]

    for idx,no in enumerate(output_neurons):
        error_at_output_layer.append((target[idx]-no.output)*no.output*(1-no.output))

    for idxno,no in enumerate(output_neurons):
        for idx,x in enumerate(no.inputs):
            no.weights[idx]=no.weights[idx]+LEARNING_RATE*error_at_output_layer[idxno]*x
    return output_neurons,error_at_output_layer

#volver
def err_hidden_layer_mas_interna(t,neurons_hidden,neurons_output,error_at_output_layer):
    error_at_hidden_layer=[]

    for idx,nh in enumerate(neurons_hidden):
        suma=0
        for idxno, no in enumerate(neurons_output):
            suma=suma+error_at_output_layer[idxno]*no.weights[idxno]
        error_at_hidden_layer.append((1-nh.output)*(nh.output)*suma)

    for idxnh,nh in enumerate(neurons_hidden):
        for idx,x in enumerate(nh.inputs):
            nh.weights[idx]=nh.weights[idx]+LEARNING_RATE*error_at_hidden_layer[idxnh]*x
    return neurons_hidden,error_at_hidden_layer

def err_hidden_layer_externas(t,neurons_hidden,neurons_output,error_at_output_layer):
    error_at_hidden_layer=[]

    for idx,nh in enumerate(neurons_hidden):
        suma=0
        for idxno, no in enumerate(neurons_output):
            suma=suma+error_at_output_layer[idxno]*no.weights[idxno]
        error_at_hidden_layer.append((1-nh.output)*(nh.output)*suma)

    for idxnh,nh in enumerate(neurons_hidden):
        for idx,x in enumerate(nh.inputs):
            nh.weights[idx]=nh.weights[idx]+LEARNING_RATE*error_at_hidden_layer[idxnh]*x
    return neurons_hidden,error_at_hidden_layer

def clean_layers(list_neurons_hidden_layer,list_neurons_output_layer):
    aux=[]
    for i in range(NUMBER_OF_HIDDEN_LAYER):
        result=list(map(lambda n: n.clear_variables(),list_neurons_hidden_layer[i]))
        aux.append(result)
    list_neurons_hidden_layer=aux    
    list_neurons_output_layer=list(map(lambda n: n.clear_variables(),list_neurons_output_layer))


def main():

    training_set=read_training_set()
    validation_set=read_validation_set()

    list_neurons_hidden_layer=initialize_hidden_layer()
    list_neurons_output_layer=initialize_output_layer()

    for idx,n in enumerate(list_neurons_hidden_layer) :
        if idx==0:
            #todos los elementos menos el target
            for s in n:
                weight = [(calculate_weight()) for i in range(LINE_LEN)]
                s.set_weights(weight)
        else:
            for s in n:
                weight = [(calculate_weight()) for i in range(HIDDEN_LAYER+1)]
                s.set_weights(weight)
    
    for no in list_neurons_output_layer:
        weight=[(calculate_weight()) for i in range(HIDDEN_LAYER+1)]
        no.set_weights(weight)

    #Iniciamos Aprendizaje
    
    ronda=0
    training_complete=False
    while(not(training_complete)):
        ronda+=1

        print("Training...")
        for t in training_set:
            for nhidx,n in enumerate(list_neurons_hidden_layer) :
                for nh in n:
                    if nhidx==0:
                        for i in range(1,LINE_LEN): #La primera hidden layer lee inputs
                            nh.sum(t[i], nh.weights[i])
                        nh.sigmoid() #to do signal function maybe we should change and solve the problems of the sigmoid
                    elif nhidx!=NUMBER_OF_HIDDEN_LAYER-1 :
                        for i in range((nhidx+1)*NUMBER_OF_NODES_SMALLEST_LAYER):
                            nh.sum(list_neurons_hidden_layer[nhidx-1][i].output,nh.weights[i])
                        nh.sigmoid()

            
            for no in list_neurons_output_layer:
                for j in range(NUMBER_OF_NODES_SMALLEST_LAYER):
                    no.sum(list_neurons_hidden_layer[nhidx-1][j].output,no.weights[j])
                no.sigmoid()
        
            output=calculate_softmax(list_neurons_output_layer)
           
            
            #print("Expected result",t[COLUMN_RESULT]," Output: ", output," percentage: ",(hits/counter))
            

            # Error Output Layer
            list_neurons_output_layer,error_at_output_layer=err_output_layer(t,list_neurons_output_layer)
            
            #Error Hidden Layer máx proxima al output
            list_neurons_hidden_layer[-1],error_at_hidden_layer=err_hidden_layer_mas_interna(t,list_neurons_hidden_layer[-1],list_neurons_output_layer,error_at_output_layer)

            for i in range(NUMBER_OF_HIDDEN_LAYER-2,-1,-1):
                list_neurons_hidden_layer[i],error_at_hidden_layer=err_hidden_layer_externas(t,list_neurons_hidden_layer[i],list_neurons_hidden_layer[i+1],error_at_hidden_layer)

            clean_layers(list_neurons_hidden_layer,list_neurons_output_layer)

        

    
        hits=0
        counter=0
        print("Validation...")
        for t in validation_set:
            for nhidx,n in enumerate(list_neurons_hidden_layer) :
                for nh in n:
                    if nhidx==0:
                        for i in range(1,LINE_LEN): #La primera hidden layer lee inputs
                            nh.sum(t[i], nh.weights[i])
                        nh.sigmoid() #to do signal function maybe we should change and solve the problems of the sigmoid
                    elif nhidx!=NUMBER_OF_HIDDEN_LAYER-1 :
                        for i in range((nhidx+1)*NUMBER_OF_NODES_SMALLEST_LAYER):
                            nh.sum(list_neurons_hidden_layer[nhidx-1][i].output,nh.weights[i])
                        nh.sigmoid()

            
            for no in list_neurons_output_layer:
                for j in range(NUMBER_OF_NODES_SMALLEST_LAYER):
                    no.sum(list_neurons_hidden_layer[nhidx-1][j].output,no.weights[j])
                no.sigmoid()
        
            output=calculate_softmax(list_neurons_output_layer)
            counter+=1
            if output == t[COLUMN_RESULT]:
                hits+=1
            
            #print("Expected result",t[COLUMN_RESULT]," Output: ", output," percentage: ",(hits/counter))
            
            clean_layers(list_neurons_hidden_layer,list_neurons_output_layer)
        
        if (hits/counter >=0.75):
            training_complete=True
        else:
            print("El resultado ha sido de ",(hits/counter)*100,"% de acierto")
    testing_set=read_testing_set()
    hits=0
    counter=0
    print("Testing...")
    for t in testing_set:
        for nhidx,n in enumerate(list_neurons_hidden_layer) :
            for nh in n:
                if nhidx==0:
                    for i in range(1,LINE_LEN): #La primera hidden layer lee inputs
                        nh.sum(t[i], nh.weights[i])
                    nh.sigmoid() #to do signal function maybe we should change and solve the problems of the sigmoid
                elif nhidx!=NUMBER_OF_HIDDEN_LAYER-1 :
                    for i in range((nhidx+1)*NUMBER_OF_NODES_SMALLEST_LAYER):
                        nh.sum(list_neurons_hidden_layer[nhidx-1][i].output,nh.weights[i])
                    nh.sigmoid()

        
        for no in list_neurons_output_layer:
            for j in range(NUMBER_OF_NODES_SMALLEST_LAYER):
                no.sum(list_neurons_hidden_layer[nhidx-1][j].output,no.weights[j])
            no.sigmoid()
    
        output=calculate_softmax(list_neurons_output_layer)
        counter+=1
        if output == t[COLUMN_RESULT]:
            hits+=1
        else:
            fail=True
        print("Expected result",t[COLUMN_RESULT]," Output: ", output," percentage: ",(hits/counter))
        

        clean_layers(list_neurons_hidden_layer,list_neurons_output_layer)
    
    print("Final result: ",(hits/counter)*100,"% of hits")
main()