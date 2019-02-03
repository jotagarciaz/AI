from queue import Queue


class Node:
    node_id = 0
    object_id = 0
    father = 0
    weight = 0
    value = 0
    
    def __init__(self,father,node_id,object_id,weight,value):
        self.node_id=node_id
        self.object_id=object_id
        self.father=father
        self.weight=weight
        self.value=value
        self.t_value=value
        self.t_weight=weight



def read_file(file):
    f = open(file, "r")
    f.seek(0)
    queue = Queue(maxsize=0)  
    explored = []
    list_elements =[[]]
    arr = []
    for line in f:
        id=int(line.split(".", 1)[0])
        value= int(line.split(" ", 3)[1])
        weight=int(line.split(" ", 3)[2].split('\n', 2)[0])
        arr.append(-1)
        list_elements.append(Node(0,id,id,weight,value))
    queue.put(arr)
    lets_explore(queue,explored)
    return res

def lets_explore(queue,explored):     
    q=queue.get()
    for 
lista = subset(11)
print(lista)


