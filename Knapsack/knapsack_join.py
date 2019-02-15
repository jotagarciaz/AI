import time
start = time.time()
from queue import Queue
from copy import copy


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
    list_elements=[]
    nodes=[]
    stack=[]
    for line in f:
        id=int(line.split(".", 1)[0])
        value= int(line.split(" ", 3)[1])
        weight=int(line.split(" ", 3)[2].split('\n', 2)[0])
        nodes.append(Node(id,weight,value))
        list_elements.append(-1)
    list_elements.append(0)
    list_elements.append(0)
    
    queue.put(list_elements)
    bf=bfs(queue,nodes) 
    for i in range(0,len(bf)-2):
        if(bf[i]==1):
            node=nodes[i]
            bf[i]={"id":node.object_id,"weight":node.weight,"value":node.value}
    bf=list(filter(lambda x: x != 0, bf))
    
    value=len(bf)-1
    weight=len(bf)-2
    bf[value]={"total value":bf[value]}
    bf[weight]={"total weight":bf[weight]}

    stack.append(list_elements)
    df=dfs(stack,nodes)
    for i in range(0,len(df)-2):
        if(df[i]==1):
            node=nodes[i]
            df[i]={"id":node.object_id,"weight":node.weight,"value":node.value}
    
    df=list(filter(lambda x: x != 0, df))
    
    value=len(df)-1
    weight=len(df)-2
    df[value]={"total value":df[value]}
    df[weight]={"total weight":df[weight]}
    return bf,df



def bfs(queue,nodes):
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
                    q_positive[len(q_positive)-1]=value+nodes[i].value
                    q_positive[len(q_positive)-2]=weight+nodes[i].weight
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


def dfs(stack,nodes):
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

print("BFS: \n\n",solution[0])
print("DFS: \n\n",solution[1])    

end = time.time()
print(end - start)