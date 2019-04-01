import math
import time
start = time.time()
from copy import deepcopy 
import os
import psutil
proccess = psutil.Process(os.getpid())
import random

N_MUTANTS=5
mutants=[]
MAXIMUN_DISTANCE_ALLOWED=9000
visited=[]
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

def generate_mutants(list_points):
    variations=list_points[1:len(list_points)]
    
    for i in range(0,N_MUTANTS):
        aux=[]
        aux.append(list_points[0])
        random.shuffle(variations)
        for v in variations:
            aux.append(v)
        aux.append(list_points[0])
        mutants.append(aux)

def calculate_distance_path(mutant):
    total=0
    for p in range(1,len(mutant)):
        total=total+calculate_distance_between_points(mutant[p-1],mutant[p])
    return total 

def calculate_distance_between_points(point1,point2):
    return math.sqrt((point2.x-point1.x)**2+(point2.y-point1.y)**2)

def order_paths():
    order=[]
    for m in mutants:
        result_path=calculate_distance_path(m)
        order.append((result_path,m))
    order=sorted(order)
    
    for o in range(0,len(order)):
        mutants[o]=order[o][1]


def crossover(parent1,parent2):
    best_distance=MAXIMUN_DISTANCE_ALLOWED
    start_index=random.randrange(0,len(parent1)-2)
    finish_index=random.randrange(start_index,len(parent1)-1)
    crossover=[]
    aux=[]
    for i in range(start_index,finish_index):
        aux.append(parent1[i])
    
    
    first_time=True
    for e in parent1:
        if e not in aux:
            crossover.append(e)
        elif first_time:
            first_time=False
            for a in aux:
                crossover.append(a)
    return crossover

def mutate(crossover):
    for i in range(1,N_MUTANTS):
        mutants[i]=crossover
        random_index1 = random.randrange(1,len(mutants[i])-1)
        random_index2 = random.randrange(1,len(mutants[i])-1)
        aux=mutants[i][random_index1]
        mutants[i][random_index1]=mutants[i][random_index2]
        mutants[i][random_index2]=aux

def main():
   
    points=read_file("berlin_coordinates")
    generate_mutants(points)
    result_distance=MAXIMUN_DISTANCE_ALLOWED*100
    while result_distance>9000:
        order_paths()
        distance=calculate_distance_path(mutants[0])
        cross=crossover(mutants[0],mutants[1])
        
        if(distance<result_distance):
            result_distance=distance
            print("best distance until now: ",result_distance)
            result_path=mutants[0]
        mutate(cross)

    print("Best result distance: ",result_distance," Best result path: ",result_path)
    
    end = time.time()
    #print(end - start)
    #print(proccess.memory_info().rss)



main()
