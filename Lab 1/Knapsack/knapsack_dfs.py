import time
import os
import psutil
start = time.time()
from copy import copy


process = psutil.Process(os.getpid())
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
    stack=[]
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

    stack.append(list_elements)
    res=go_explore(stack,nodes) 
    for i in range(0,len(res)-2):
        if(res[i]==1):
            node=nodes[i]
            res[i]={"id":node.object_id,"weight":node.weight,"value":node.value}
    
    res=list(filter(lambda x: x != 0, res))
    
    value=len(res)-1
    weight=len(res)-2
    res[value]={"total value":res[value]}
    res[weight]={"total weight":res[weight]}
    return res



def go_explore(stack,nodes):
    best_value = 0
    res=[]
    while not len(stack)==0:
        s=copy(stack.pop())
        for i in range(len(s)):
            if s[i] is -1:
                weight = s[len(s)-2]
                value = s[len(s)-1]
                if weight<=420:
                    if value > best_value:
                        res = s
                        best_value=value
                    s[i]=0
                    stack.append(s)
                    s_positive= copy(s)
                    s_positive[len(s_positive)-1]=s_positive[len(s_positive)-1]+nodes[i].value
                    s_positive[len(s_positive)-2]=s_positive[len(s_positive)-2]+nodes[i].weight
                    s_positive[i]=1
                    stack.append(s_positive)
                break
            elif i == len(s)-1:
                weight = s[len(s)-2]
                value = s[len(s)-1]
                if weight<=420:
                    if value > best_value:
                        res = s
                        best_value=value
    return res            


    
solution=read_file('Knapsack/data_knapsack')


for data in solution:
    print(data)
end = time.time()
print(end - start)
print(process.memory_info().rss)