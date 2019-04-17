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


hidden_layer_1_neurons = 20 #number of hidden layers neurons
hidden_layer_2_neurons = 10
output_neurons = 10

LEARNING_RATE=0.1

#lr=0.1 #Setting learning rate
#Variable initialization
#epoch=5000 #Setting training iterations

def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
""" First we need to extract values from the file"""
def read_training_set():
    n_lines_training = int(PERCENTAGE_TRAINING * n_lines_to_read) 
  
    f.seek(0)
    resultado_training=np.zeros(n_lines_training)
    training_set=np.zeros((n_lines_training,LINE_LEN-1))
    for i in range(0, n_lines_training): #n_lines_training):
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(1,len(aux)):
            line[j-1]=(num(aux[j])/255)
            
        training_set[i]=line.copy()
        resultado_training[i]=int(aux[0])
             
    return training_set,resultado_training

def read_validation_set():
    n_lines_validation = int(PERCENTAGE_VALIDATION * n_lines_to_read) #3 
  
    f.seek(0)
    resultado_validation =np.zeros(n_lines_validation)
    validation_set=np.zeros((n_lines_validation,LINE_LEN-1))
    for i in range(0, n_lines_validation): #n_lines_training):
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(1,len(aux)):
            line[j-1]=(num(aux[j])/255)
            
        validation_set[i]=line.copy()
        resultado_validation[i]=int(aux[0])
             
    return validation_set,resultado_validation

def read_testing_set():
    n_lines_testing = int(PERCENTAGE_TEST * n_lines_to_read) #3 
  
    f.seek(0)
    resultado_testing =np.zeros(n_lines_testing)
    testing_set=np.zeros((n_lines_testing,LINE_LEN-1))
    for i in range(0, n_lines_testing): #n_lines_training):
        aux = f.readline()
        aux=aux.split(",", LINE_LEN)
        line=np.zeros(len(aux)-1)
        for j in range(1,len(aux)):
            line[j-1]=(num(aux[j])/255)
            
        testing_set[i]=line.copy()
        resultado_testing[i]=int(aux[0])
             
    return testing_set,resultado_testing


def sigmoid(net):
  return 1/(1+np.exp(-net)) 

def softmax(output):

    softmax = np.exp(output)
    suma=np.sum(softmax)
    softmax=softmax[0]/suma
    output=softmax.argmax(axis=0)
    return output,softmax


def main():
    target_error = np.zeros((output_neurons,output_neurons))
    np.fill_diagonal(target_error,1)
    

    datos_training,resultado_training=read_training_set()
    datos_validation,resultado_validation=read_validation_set()

     #weight and bias initialization
    weights_hidden_layer_1=np.random.uniform(-1,1,size=(LINE_LEN-1,hidden_layer_1_neurons))
    bias_hidden_layer_1=np.random.uniform(-1,1,size=(1,hidden_layer_1_neurons))
    
    weights_hidden_layer_2=np.random.uniform(-1,1,size=(hidden_layer_1_neurons,hidden_layer_2_neurons))
    bias_hidden_layer_2=np.random.uniform(-1,1,size=(1,hidden_layer_2_neurons))
   
    weights_output_layer=np.random.uniform(-1,1,size=(hidden_layer_2_neurons,output_neurons))
    bias_out=np.random.uniform(-1,1,size=(1,output_neurons))
    hits=0

    counter=0
    while hits/len(datos_validation) < 0.8:
        hits=0
      

        #training
        for x in range(len(datos_training)):
            inputlayer_neurons = datos_training[x]

            #Forward Propogation
            hidden_layer_input_net_sum=np.dot(inputlayer_neurons,weights_hidden_layer_1)
            hidden_layer_input=hidden_layer_input_net_sum + bias_hidden_layer_1
            hidden_layer_1_activations = sigmoid(hidden_layer_input)
            
            hidden_layer_2_input_net_sum=np.dot(hidden_layer_1_activations,weights_hidden_layer_2)
            hidden_layer_2_input=hidden_layer_2_input_net_sum + bias_hidden_layer_2
            hidden_layer_2_activations = sigmoid(hidden_layer_2_input)
            
            output_layer_input_net_sum=np.dot(hidden_layer_2_activations ,weights_output_layer)
            output_layer_input= output_layer_input_net_sum+ bias_out
            
            result_output, output_softmax= softmax(output_layer_input)

            #Backpropagation
            E = target_error[int(resultado_training[x])]-output_softmax

            d_output = E*output_softmax * (1- output_softmax)
            
            Error_at_hidden_layer_2 = d_output.dot(weights_output_layer.T)
            d_hidden_layer_2 = (Error_at_hidden_layer_2 * hidden_layer_2_activations)*(1-hidden_layer_2_activations)
        
            Error_at_hidden_layer_1 = d_hidden_layer_2.dot(weights_hidden_layer_2.T)
            d_hidden_layer_1 = (Error_at_hidden_layer_1 * hidden_layer_1_activations)*(1-hidden_layer_1_activations)

            weights_output_layer = weights_output_layer + hidden_layer_2_activations.T.dot(np.reshape(d_output,(1,output_neurons))) *LEARNING_RATE
            bias_out = bias_out + np.sum(d_output, axis=0,keepdims=True) * LEARNING_RATE
            
            weights_hidden_layer_2 = weights_hidden_layer_2 + hidden_layer_1_activations.T.dot(d_hidden_layer_2) *LEARNING_RATE
            bias_hidden_layer_2 = bias_hidden_layer_2 + np.sum(d_hidden_layer_2, axis=0,keepdims=True) *LEARNING_RATE

            weights_hidden_layer_1 = weights_hidden_layer_1 + np.reshape(datos_training[x],(1,LINE_LEN-1)).T.dot(d_hidden_layer_1) *LEARNING_RATE
            bias_hidden_layer_1 += np.sum(d_hidden_layer_1, axis=0,keepdims=True) *LEARNING_RATE
            
            
        
        for x in range(len(datos_validation)):
            inputlayer_neurons = datos_validation[x]

            #Forward Propogation
            hidden_layer_input_net_sum=np.dot(inputlayer_neurons,weights_hidden_layer_1)
            hidden_layer_input=hidden_layer_input_net_sum + bias_hidden_layer_1
            hidden_layer_1_activations = sigmoid(hidden_layer_input)
            
            hidden_layer_2_input_net_sum=np.dot(hidden_layer_1_activations,weights_hidden_layer_2)
            hidden_layer_2_input=hidden_layer_2_input_net_sum + bias_hidden_layer_2
            hidden_layer_2_activations = sigmoid(hidden_layer_2_input)
            
            output_layer_input_net_sum=np.dot(hidden_layer_2_activations ,weights_output_layer)
            output_layer_input= output_layer_input_net_sum+ bias_out
            
            result_output, output_softmax= softmax(output_layer_input)
            
            if result_output== int(resultado_validation[x]):
                hits=hits+1

        print("porcentaje de acierto Validation= ",(hits/len(datos_validation))*100," ronda= ",counter)
        counter=counter+1
    
    print("Leyendo datos de testing")
    datos_testing,resultado_testing=read_testing_set()
    hits=0
    for x in range(len(datos_testing)):
        inputlayer_neurons = datos_testing[x]

        #Forward Propogation
        hidden_layer_input_net_sum=np.dot(inputlayer_neurons,weights_hidden_layer_1)
        hidden_layer_input=hidden_layer_input_net_sum + bias_hidden_layer_1
        hidden_layer_1_activations = sigmoid(hidden_layer_input)
        
        hidden_layer_2_input_net_sum=np.dot(hidden_layer_1_activations,weights_hidden_layer_2)
        hidden_layer_2_input=hidden_layer_2_input_net_sum + bias_hidden_layer_2
        hidden_layer_2_activations = sigmoid(hidden_layer_2_input)
        
        output_layer_input_net_sum=np.dot(hidden_layer_2_activations ,weights_output_layer)
        output_layer_input= output_layer_input_net_sum+ bias_out
        
        result_output, output_softmax= softmax(output_layer_input)
        
        if result_output== int(resultado_testing[x]):
            hits=hits+1

    print("porcentaje de acierto Testing= ",(hits/len(datos_testing))*100)
 
main()