import time
start = time.time()
from copy import deepcopy


""" First we need to extract values from the file"""
def read_file(file):
    f = open(file, "r")
    f.seek(0)
    stack=[]
    sudokus = []
    matrix = []
    res = []
    i=0
    for line in f:
        if not (line.find("SUDOKU")!=-1 or line=="\n"):

            line = line[0:9]
            aux=list(map(lambda x: int(x), line))
            matrix.append(aux)
            i+=1
            if(i==9):
                sudokus.append(matrix)
                matrix=[]
                i=0
            
            
    for sudoku in sudokus:  
        aux = deepcopy(sudoku)
        for row in aux:
            for i in range(9):
                if row[i]==0:
                    row[i] = posible_combinations(aux,aux.index(row),row,i)
                    
        sudoku,aux,stack=next_step(sudoku,aux,stack)
        res.append(go_explore(stack,aux))

    for r in res:    
        print(r,"\n\n")
        
def next_step(sudoku,aux,stack):
    beginby=[1,2,3,4,5,6,7,8,9]
    rowbegin=0
    columnbegin=0
    for row in aux:
        for element in row:
            if isinstance(element,list):
                if len(element)==1:  
                    sudoku[aux.index(row)][row.index(element)]=element[0]
                    element=element.pop()
                elif len(element) < len(beginby):
                    beginby=element
                    rowbegin=aux.index(row)
                    columnbegin = row.index(element)
    if len(beginby)<9:
        element=posible_combinations(aux,rowbegin,aux[rowbegin],columnbegin)
        for b in element:
            sudoku[rowbegin][columnbegin] = b
            stack.append(deepcopy(sudoku))

    return sudoku,aux,stack 


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
            
def go_explore(stack,aux):

    while not len(stack)==0:
        s=stack.pop()
        s,aux,stack=next_step(s,aux,stack)
        if(len(stack)==0):
            res=s
    return res       



read_file("Sudoku/sudoku")
end = time.time()
print(end - start)