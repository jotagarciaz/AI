import time
start = time.time()
from copy import copy

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
        resolve_sudoku(sudoku)
        print("\n\n")
    
def resolve_sudoku(sudoku):
    for row in sudoku:
        for i in range(0,9):
            if row[i]==0:
                row[i] = posible_combinations(sudoku,sudoku.index(row),row,i)
    print(sudoku)

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
            
                    
read_file("Sudoku/sudoku")
end = time.time()
print(end - start)