from queue import Queue

NODE_NUMBER = 0

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


""" First we need to extract values from the file"""
def read_file(file):
    f = open(file, "r")
    f.seek(0)
    queue=Queue(maxsize=0)  
    explored = [Node(0,0,0,0,0)]
    list_elements=[]
    for line in f:
        id=int(line.split(".", 1)[0])
        value= int(line.split(" ", 3)[1])
        weight=int(line.split(" ", 3)[2].split('\n', 2)[0])
        queue.put(Node(0,id,id,weight,value)) 
        list_elements.append(Node(0,id,id,weight,value))
    
    global NODE_NUMBER 
    NODE_NUMBER  = len(list_elements)+1
    res = bfs(list_elements,queue,explored)
    return res



def bfs(list_elements,queue,explored):
    m=explore(list_elements,queue,explored)
    queue=m[0]
    explored=m[1]
    if queue.empty:
        res=explored[0]
        while len(explored)>0:
            aux=explored.pop()
            if(aux.t_value>res.t_value):
                res=aux
    return res


def explore(list_elements,queue,explored):
    while not queue.empty():
        q = queue.get()
        aux=explored[q.father]
        q.t_weight=q.weight+aux.t_weight
        global NODE_NUMBER
        if(q.t_weight<=420):
            q.t_value=q.value+aux.t_value
            for l in list_elements:
                aux=q
                exist=False 
                while(aux.node_id != 0 ):
                    if l.object_id!=aux.object_id:
                        aux=explored[aux.father]
                    else:
                        exist=True
                        break
                if not exist:
                    queue.put(Node(q.node_id,NODE_NUMBER,l.object_id,l.weight,l.value))
                    NODE_NUMBER+=1
            explored.append(q)  
    return queue,explored    
       
            


    
data=read_file('data_knapsack')
print(data.t_value)

