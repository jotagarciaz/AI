import time
start = time.time()
from copy import deepcopy

"""
No comprobar al principio, en el DFS vamos buscando 0 y por cada 0 buscamos las posibles combinaciones, las metemos en el stack
sino hay posibles combinaciones la solución se anula, si no hay 0 entonces hemos encontrado solución.
"""
""" First we need to extract values from the file"""
def read_file(file):
    f = open(file, "r")
    f.seek(0)
    stack=[]
    sudokus = []
    matrix = []
    i=0
    for line in f:
        if(line.find("SUDOKU")!=-1 or line=="\n"):
            i=0
            continue
        else:
            line = line[0:9]
            aux=list(map(lambda x: int(x), line))
            matrix.append(aux)
            if(i==8):
                sudokus.append(matrix)
                matrix=[]
            i+=1
    
    for sudoku in sudokus:
        res=resolve_sudoku(sudoku)
        print(res)
        print("\n\n")
        
    

def posible_combinations(sudoku,row_index,row,column_index):
    first_row = int(row_index/3)
    first_column= int(column_index/3)
    mat3_3=[]
    column=[]
    res=[]
    for i in range(first_row*3,(first_row+1)*3):
        for j in range(first_column*3,(first_column+1)*3):
            mat3_3.append(sudoku[i][j])
    
    for r in sudoku:
        column.append(r[column_index])
    
    for i in range(1,10):
        if i not in row and i not in mat3_3 and i not in column:
            res.append(i)
    return res
            
def go_explore(stack):

    while not len(stack)==0:
        s=stack.pop()
        complete = True
        for row in s:
            if not complete:
                break
            for i in range(0,9):
                if row[i]==0:
                    complete= False
                    aux = posible_combinations(s,s.index(row),row,i)
                    if len(aux)>0:
                        for a in aux:
                            row[i] = a
                            saux=deepcopy(s)
                            stack.append(saux)
                    break

        if complete:        
            res=s
            return res
    return res       

def resolve_sudoku(sudoku):
    stack = []
    stack.append(sudoku)
    res = go_explore(stack)
    return res

read_file("Sudoku/sudoku")
end = time.time()
print(end - start)