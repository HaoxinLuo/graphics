def createM(n):
    tmp = []
    for x in range(n):
        tmp.append([0,0,0,0])
    return tmp

def deleteM():
    return None

def idenM():
    tmp = createM(4)
    for i in range(4):
        setM(tmp,i,i,1)
    return tmp

def setM(m,c,r,v):
    m[c][r] = v
    
def copyM(m):
    tmp = createM(len(m))
    for x in range(len(m)):
        for y in range(4):
            setM(tmp,x,y,m[x][y])
    return tmp

def copyCol(m,c):
    tmp = createM(1)
    setM(tmp,0,0,getM(m,c,0))
    setM(tmp,0,1,getM(m,c,1))
    setM(tmp,0,2,getM(m,c,2))
    setM(tmp,0,3,getM(m,c,3))
    return tmp[0]

def addCol(m):
    m.append([0,0,0,0])

def getM(m,c,r):
    return m[c][r]

def printM(m,n):
    col = ""
    print n
    for y in range(len(m[0])):
        for x in range(len(m)):
            col = col + ' '+ str(m[x][y])
        print col
        col = ""

def multiM(m,m2):
    tmp = createM(len(m2))
    for y in range(4):
        for x in range(len(tmp)):
            col = [m2[x][c] for c in range(len(m2[0]))]
            row = [m[r][y] for r in range(len(m))]
            tmp[x][y] = sum([r*c for (r,c) in zip(row,col)])
    return tmp
            
