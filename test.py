mat=[]
m = 5
n = 6
row = [i for i in range(n+1)]
for i in range (0,m+1):
    print(i)
    row[0] = i
    print(row)
    print(mat)
    rowc= row.copy()
    mat= mat+[rowc]
    # mat.extend
#     row = [0,1,2,3,4,5]
    
