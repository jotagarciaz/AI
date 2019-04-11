import math
import time
start = time.time()
from copy import deepcopy 
import os
import psutil
proccess = psutil.Process(os.getpid())
import random
from functools import reduce
import matplotlib.pyplot as plt

N_MUTdistances=52
ANTS_NUMBER=150
PHEROMONE_INIT_VALUE=10
MAXIMUN_DISTANCE_ALLOWED=7500
alpha= 1
beta=2
PROBABILITY = 0.995

list_points=[] #list of points received from the file
pheromone=[[(PHEROMONE_INIT_VALUE if i is not j else 0) for i in range(N_MUTdistances)] for j in range(N_MUTdistances)]
distances=[]
heuristic=[]
L=[]
cost = []


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
    global list_points
    global N_MUTdistances
    f = open(file, "r")
    f.seek(0)
    

    for line in f:
        splt = line.split(" ",3)
        id = int(splt[0])
        x = float(splt[1])
        y = float(splt[2].split('\n', 2)[0])
        list_points.append(Point(id,x,y))
    
    N_MUTdistances=len(list_points)

def calculate_distance_between_points(point1,point2):
    return math.sqrt((point2.x-point1.x)**2+(point2.y-point1.y)**2)

def calculate_distances():
    global distances
    for i in list_points:
        aux=[] 
        for j in list_points:
            if i == j:
                aux.append(math.inf)
            else:
                d=calculate_distance_between_points(i,j)
                aux.append(d)
        distances.append(aux)

def not_zero_division_heuristic(x):
   return  1/x if x is not 0 else 0

def calculate_heuristic():
    global heuristic
    for l in distances:
        heuristic.append(list(map(lambda x: not_zero_division_heuristic(x), l)))


def transition_rule(path):
    sum=0
    calculate_probabilistic_s=[]
    r = path[-2]
    index_r=list_points.index(r)
    not_visited=[]
    for i in list_points:
        if i not in path:
            not_visited.append(i)
            sum+= (pheromone[index_r][list_points.index(i)]**alpha)*(heuristic[index_r][list_points.index(i)]**beta)
    for i in not_visited:
        calculate_probabilistic_s.append(((pheromone[index_r][list_points.index(i)]**alpha)*(heuristic[index_r][list_points.index(i)]**beta))/sum)
    
    
    sum_fit=reduce((lambda x,y: x+y),calculate_probabilistic_s)
    calculate_probabilistic_s= list(map(lambda x: x/sum_fit, calculate_probabilistic_s))

    index=random.random()
    sum = 0
    counter=0
    while index>sum:
        sum = sum + calculate_probabilistic_s[counter]
        counter+=1

    return not_visited[counter-1]
    


def calculate_distance_path(l):
    total=0
    for p in range(1,len(l)):
        total=total+calculate_distance_between_points(l[p-1],l[p])
    return total 

def pheromone_update():
    global pheromone
    global list_points
    global cost
    global L

    for i in range(len(pheromone)):
        for j in range(len(pheromone)):
            sum=0
            for k in L:
                    city_i = list_points[i]
                    city_j = list_points[j]
                    if k.index(city_i) is (k.index(city_j)-1):
                        sum+=1/cost[L.index(k)]
            pheromone[i][j]=((1-PROBABILITY)*pheromone[i][j])+sum

def pheromone_update_global(best_path):
    global pheromone
    global list_points
    global cost

    for i in range(len(pheromone)):
        for j in range(len(pheromone)):
            sum=0
            city_i = list_points[i]
            city_j = list_points[j]
            if best_path.index(city_i) is (best_path.index(city_j)-1):
                sum+=1/cost[L.index(best_path)]
            pheromone[i][j]=((1-PROBABILITY)*pheromone[i][j])+sum

def main():
    global list_points
    global pheromone
    global cost
    global L
    best_distance = MAXIMUN_DISTANCE_ALLOWED * 100
    best_path=[]
    best_actual_path=[]

    read_file("berlin_coordinates")
    calculate_distances()
    calculate_heuristic()
    graph_distances=[]
    graph_counter=[]

    generation=0
    cost=[]
    while best_distance > MAXIMUN_DISTANCE_ALLOWED:
        L.clear()
        for k in range(ANTS_NUMBER):
            L.append([list_points[0],list_points[0]])
        cost.clear()
        best_actual_distance = best_distance
        
        for j in range(N_MUTdistances-1):
            for i in range(ANTS_NUMBER):
                L[i].insert(-1,transition_rule(L[i]))

        for i in range(ANTS_NUMBER):
            actual_distance = calculate_distance_path(L[i])
            
            cost.append(actual_distance)
            if actual_distance < best_actual_distance:
                best_actual_distance = actual_distance
                best_actual_path = L[i]
        
        pheromone_update()       

        if best_actual_distance<best_distance: 
            best_distance = best_actual_distance
            best_path = best_actual_path
            print("Actual best distance: ",best_distance," generation: ",generation)
            pheromone_update_global(best_path)
            graph_distances.append(best_actual_distance)
            graph_counter.append(generation)
        generation +=1

    print("best distance: ",best_distance," best path: ",best_path)
    """plt.plot(graph_counter,graph_distances)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()"""

    end = time.time()
    print(end - start)
    print(proccess.memory_info().rss)
main()