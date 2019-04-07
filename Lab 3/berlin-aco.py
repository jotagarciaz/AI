import math
import time
start = time.time()
from copy import deepcopy 
import os
import psutil
proccess = psutil.Process(os.getpid())
import random

N_MUTdistances=53
PHEROMONE_INIT_VALUE=10

distances=[ [0 for i in range(N_MUTdistances)] for j in range(N_MUTdistances)]
heuristic=[]
pheromone=[[(PHEROMONE_INIT_VALUE if i is not j else 0) for i in range(N_MUTdistances)] for j in range(N_MUTdistances)]
cost=[]
list_points=[]
actual_best_distance=[]

MAXIMUN_DISTANCE_ALLOWED=9000
MAXIMUN_GENERATIONS_EXTRA=5000
alpha =0.5
beta= 1-alpha

class Point:
    id=0
    x=0
    y=0
    
    def __init__(self,id,x,y):
        self.id=id
        self.x=x
        self.y=y 
    
    def __repr__(self):
        return "id: %i" % (self.id)    
    def __str__(self):
        return "id: %i" % (self.id)            

def read_file(file):
    f = open(file, "r")
    f.seek(0)
    list_points=[]

    for line in f:
        splt = line.split(" ",3)
        id = int(splt[0])
        x = float(splt[1])
        y = float(splt[2].split('\n', 2)[0])
        list_points.append(Point(id,x,y))
    
    return list_points

def calculate_distance_path(mutant):
    total=0
    for p in range(1,len(mutant)):
        total=total+calculate_distance_between_points(mutant[p-1],mutant[p])
    return total 

def calculate_distance_between_points(point1,point2):
    return math.sqrt((point2.x-point1.x)**2+(point2.y-point1.y)**2)

def calculate_distances(list_points):
    global distances
    aux=[]
    for i in list_points:
        for j in list_points:
            aux.append(calculate_distance_between_points(i,j))
        distances.append(aux)

def not_zero_division_heuristic(x):
   return  1/x if int(x) is not 0 else 0

def calculate_heuristic():
    global heuristic
    for l in distances:
        heuristic.append(list(map(lambda x: not_zero_division_heuristic(x), l)))


#¿t? recieves  destination city s p no es un aleatorio
def pheromone_update(s,iteration,distances,cost):
    global pheromone
    global list_points
    result=0
    for i in range(len(list_points)):
        result+=1/cost[i][s]
    
    for i in range(len(list_points)):
        p=random.random()
        pheromone[i][s]=(1-p)*pheromone[i][s]*(iteration-1)+result

def transition_rule(r,p,h):
    sum=0
    calculate_probabilistic_s=[]
    for i in list_points:
        if i not in r:
            sum+= p[i]**alpha+h[i]**beta
    for i in list_points:
        if i not in r:
            calculate_probabilistic_s.append((p[i]**alpha+h[i]**beta)/sum)
    
    index=random.random()
    sum = 0
    counter=0
    while index>sum:
        sum = sum + calculate_probabilistic_s[counter]
        counter+=1

    return counter-1



def main():
    global list_points
    points=read_file("berlin_coordinates")
    calculate_distances(points)
    
    
    #initialize distances

    for i in range(0,len(points)):
        distances[i] = points[0]
        
    calculate_heuristic()

    result_distance=MAXIMUN_DISTANCE_ALLOWED*100
    iteration=0

    while(result_distance>9000):
        

        #build the solutions
        for i in range(1,len(points)):
            for k in range(len(distances)):
                distances[k][i]=transition_rule(distances[k],pheromone[k],heuristic[k])


        
        mejor_coste=MAXIMUN_DISTANCE_ALLOWED*100
        #calculate the total cost of the distances and the best ant
        for i in range(len(distances)):
            coste = calculate_distance_path(distances[i])
            cost.append(coste)
            if coste < mejor_coste:
                actual_best_distance = distances[i]
                mejor_coste=coste

        for i in range(0, len(distances)):
            for j in range(0, len(distances)):
                pheromone_update(distances[k][-1],iteration,distances,cost)

        if mejor_coste < result_distance :
            result_distance=mejor_coste
            result_path=actual_best_distance

        print("Best result distance: ",result_distance," Best result path: ",result_path)

        iteration+=1
    print("Distance: ",result_distance," Path: ",result_path)
    end = time.time()
    print(end - start)
    print(proccess.memory_info().rss)



main()
