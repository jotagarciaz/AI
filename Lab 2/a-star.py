from copy import deepcopy 

""" First we need to extract values from the file"""
def read_files(file1,file2):

    f = open(file1, "r") #city_road
    f2 = open(file2, "r")  #straight
    f.seek(0)
    nodes={}
    for line in f:
        line_split=line.split(" ", 3)
        origin=line_split[0]
        destiny= line_split[1]
        distance=int(line_split[2])
        route= {destiny:distance}
        route_inverse={origin:distance}
        if destiny not in nodes:
            nodes.update({destiny:route_inverse})
        else:
            nodes[destiny].update(route_inverse)
        if origin not in nodes:
            nodes.update({origin:route})
        else:
            nodes[origin].update(route)
    
    real=deepcopy(nodes)
    straight={}
    for line in f2:
        line_split=line.split(" ", 2)
        city=line_split[0]
        distance=int(line_split[1])
        straight.update({city:distance})
    
    for k,n in nodes.items():
        for destiny in n:
            n[destiny]=straight[destiny]+n[destiny]
        n = sorted(n.items(), key=lambda x:x[1])
        nodes[k]=n
    
    nodes=aStar(nodes,real)
    return nodes

def aStar(nodes,real):
    path=[["Malaga"],[]]
    last_visited=path[0][-1]
    while last_visited != 'Valladolid':
        for city,distance in nodes[last_visited]:
            if city not in path[0]:
                path[0].append(city)
                path[1].append(real[last_visited][city])
                break
        last_visited=path[0][-1]
    return path 
        
print(read_files("city_roads","straight_city"))