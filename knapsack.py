import time
start = time.time()
from queue import Queue
from copy import copy,deepcopy


NODE_NUMBER = 0

class Node:
    object_id = 0
    weight = 0
    value = 0
    
    def __init__(self,object_id,weight,value):
        self.object_id=object_id
        self.weight=weight
        self.value=value



""" First we need to extract values from the file"""
def read_file(file):
    f = open(file, "r")
    f.seek(0)
    queue=Queue(maxsize=0)  
    explored = []
    list_elements=[]
    nodes=[]
    for line in f:
        id=int(line.split(".", 1)[0])
        value= int(line.split(" ", 3)[1])
        weight=int(line.split(" ", 3)[2].split('\n', 2)[0])
        nodes.append(Node(id,weight,value))
        list_elements.append(-1)
    list_elements.append(0)
    list_elements.append(0)

    queue.put(list_elements)
    res=go_explore(queue,explored,nodes) 
    for i in range(0,len(res)-2):
        if(res[i]==1):
            node=nodes[i]
            res[i]={"id":node.object_id,"weight":node.weight,"value":node.value}
    for i in range(0,len(res)-2):
        if(res[i]==0):
            res.pop(i)
    
    value=len(res)-1
    weight=len(res)-2
    res[value]={"total value":res[value]}
    res[weight]={"total weight":res[weight]}
    return res



def go_explore(queue,explored,nodes):
    best_value = 0
    res=[]
    while not queue.empty():
        q=copy(queue.get())
        for i in range(len(q)):
            if q[i] is -1:
                weight = q[len(q)-2]
                value = q[len(q)-1]
                if weight<=420:
                    if value > best_value:
                        res = q
                        best_value=value
                    q[i]=0
                    queue.put(q)
                    q_positive= copy(q)
                    q_positive[len(q_positive)-1]=q_positive[len(q_positive)-1]+nodes[i].value
                    q_positive[len(q_positive)-2]=q_positive[len(q_positive)-2]+nodes[i].weight
                    q_positive[i]=1
                    queue.put(q_positive)
                break
            elif i == len(q)-1:
                weight = q[len(q)-2]
                value = q[len(q)-1]
                if weight<=420:
                    if value > best_value:
                        res = q
                        best_value=value
    return res            


    
solution=read_file('data_knapsack')
for data in solution:
    print(data)
end = time.time()
print(end - start)
