import math
import time
start = time.time()
from copy import deepcopy 
import os
import psutil
proccess = psutil.Process(os.getpid())
splt
class Point:
    id=0
    x=0
    y=0
    
    def __init__(self,id,x,y):
        self.id=id
        self.x=x
        self.y=y
        

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

def calculate_distance(point1,point2):
    return math.sqrt((point2.x-point1.x)**2+(point2.y-point1.y)**2)

end = time.time()
print(end - start)
points=read_file("berlin_coordinates")

print(calculate_distance(points[0],points[1]))

print(proccess.memory_info().rss)