from matrix import *
from math import cos,sin,radians
import sys, math

edge = createM(0)
trans = idenM()
screen = []
pix = []

def main():
    if(len(sys.argv)<2):
        print("no file name given")
        exit(0)
    f = open(sys.argv[1],'r')
    global trans,edge,screen,pix
    while(True):
        cache = f.readline().split()
        cache[1:]=[float(q) if not(cache[0]=='file' or cache[0]=='#') else q for q in cache[1:]]
        if cache[0] == '#':
            pass
        elif cache[0] == 'line':
            addLine(cache[1],cache[2],cache[3],cache[4],cache[5],cache[6])
        elif cache[0] == 'identity':
            trans = idenM()
        elif cache[0] == 'move':
            move(cache[1],cache[2],cache[3])
        elif cache[0] == 'scale':
            scale(cache[1],cache[2],cache[3])
        elif cache[0] == 'rotate-x':
            rotate(cache[1],0)
        elif cache[0] == 'rotate-y':
            rotate(cache[1],1)
        elif cache[0] == 'rotate-z':
            rotate(cache[1],2)
        elif cache[0] == 'screen':
            screen = cache[1:]
        elif cache[0] == 'pixels':
            for x in range(int(cache[1])):
                pix.append([])
                for y in range(int(cache[2])):
                    pix[x].append('0 0 0')
        elif cache[0] == 'transform':
            edge = multiM(trans,edge)
            printM(edge,'edgeA')
        elif cache[0] == 'render-parallel':
            drawP(edge)
        elif cache[0] == 'clear-edges':
            edge = createM(0)
        elif cache[0] == 'clear-pixels':
            d = [len(pix),len(pix[0])]
            for x in range(d[0]):
                for y in range(d[1]):
                    pix[x][y] = '0 0 0'
        elif cache[0] == 'file':
            n = open(cache[1],'w')
            n.write("P3\n "+str(len(pix))+' '+str(len(pix[0]))+"\n 255\n")
            for y in range(len(pix[0])):
                for x in range(len(pix)):
                    n.write(pix[x][y] + ' ')
        elif cache[0] == 'end':
            break
        else:
            pass

def addLine(x,y,z,a,b,c):
    global edge
    addCol(edge)
    addCol(edge)
    setM(edge,len(edge)-2,0,x)
    setM(edge,len(edge)-2,1,y)
    setM(edge,len(edge)-2,2,z)
    setM(edge,len(edge)-2,3,1)

    setM(edge,len(edge)-1,0,a)
    setM(edge,len(edge)-1,1,b)
    setM(edge,len(edge)-1,2,c)
    setM(edge,len(edge)-1,3,1)

def move(x,y,z):
    global trans
    tmp = idenM()
    setM(tmp,3,0,x)
    setM(tmp,3,1,y)
    setM(tmp,3,2,z)
#    trans = multiM(trans,tmp)
    trans = multiM(tmp,trans)

def scale(x,y,z):
    global trans
    tmp = idenM()
    setM(tmp,0,0,x)
    setM(tmp,1,1,y)
    setM(tmp,2,2,z)
#    trans = multiM(trans,tmp)
    trans = multiM(tmp,trans)

def rotate(a,d):
    global trans
    tmp = idenM()
    if d == 0: #about x-axis
        setM(tmp,1,1,cos(radians(a)))
        setM(tmp,1,2,sin(radians(a)))
        setM(tmp,2,1,-sin(radians(a)))
        setM(tmp,2,2,cos(radians(a)))
    elif d == 1: #about y-axis
        setM(tmp,0,0,cos(radians(a)))
        setM(tmp,0,2,-sin(radians(a)))
        setM(tmp,2,0,sin(radians(a)))
        setM(tmp,2,2,cos(radians(a)))
    elif d == 2: #about z-axis
        setM(tmp,0,0,cos(radians(a)))
        setM(tmp,1,0,-sin(radians(a)))
        setM(tmp,0,1,sin(radians(a)))
        setM(tmp,1,1,cos(radians(a)))
    trans = multiM(tmp,trans)

def drawLine(A,B,C,D):
    x1 = A
    y1 = B
    x2 = C
    y2 = D
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    global pix    
    if (dx==0 and dy==0):
        plot(x1,y1)
    elif (dy==0):
        
        for x in range(min(x1,x2+1),max(x1,x2+1)):
            plot(x,y1)
    elif (dx == 0):        
        for y in range(min(y1,y2+1),max(y1,y2+1)):
            plot(x1,y)            
    elif (dy <= dx): #dx > dy
        if x1 > x2:
            x1,y1,x2,y2 = C,D,A,B
        slope = (x2 - x1)/2
        if y1 < y2:
            inc = 1
        else:
            inc = -1
        y = y1
        for x in range(x1,x2+1):
            plot(x,y)
            slope = slope - dy
            if slope < 0:
                y = y + inc
                slope = slope + dx
    elif (dy > dx): #y major
        if y1 > y2:
            x1,y1,x2,y2 = C,D,A,B
        slope = (y2-y1)/2
        if x1 < x2:
            inc = 1
        else:
            inc = -1
        x = x1
        for y in range(y1,y2+1):
            plot(x,y)
            slope = slope - dx
            if slope < 0:
                x = x + inc
                slope = slope + dy


def plot(x,y):
    global pix
    if (x>= 0 and x<=len(pix)) and (y>= 0 and y<=len(pix[0])):
        pix[x][y] = '255 255 255'


def drawP(m):
    i = 0
    xl = screen[0]
    yb = screen[1]
    xr = screen[2]
    yt = screen[3]
    pxl = 0
    pxr = len(pix)
    pyt = 0
    pyb = len(pix[0])
    while(i+1<len(m)):
        A = ( ( (m[i][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
        B = ( ( (m[i][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
        C = ( ( (m[i+1][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
        D = ( ( (m[i+1][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
        i = i + 2
        if i<=8 or (i>16 and i<=28):
            drawLine(int(A),int(B),int(C),int(D))
        else:
            drawLine2(int(A),int(B),int(C),int(D))

def drawLine2(A,B,C,D):
    x1 = A
    y1 = B
    x2 = C
    y2 = D
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    global pix    
    if (dx==0 and dy==0):
        plot2(x1,y1)
    elif (dy==0):
        
        for x in range(min(x1,x2+1),max(x1,x2+1)):
            plot2(x,y1)
    elif (dx == 0):        
        for y in range(min(y1,y2+1),max(y1,y2+1)):
            plot2(x1,y)            
    elif (dy <= dx): #dx > dy
        if x1 > x2:
            x1,y1,x2,y2 = C,D,A,B
        slope = (x2 - x1)/2
        if y1 < y2:
            inc = 1
        else:
            inc = -1
        y = y1
        for x in range(x1,x2+1):
            plot2(x,y)
            slope = slope - dy
            if slope < 0:
                y = y + inc
                slope = slope + dx
    elif (dy > dx): #y major
        if y1 > y2:
            x1,y1,x2,y2 = C,D,A,B
        slope = (y2-y1)/2
        if x1 < x2:
            inc = 1
        else:
            inc = -1
        x = x1
        for y in range(y1,y2+1):
            plot2(x,y)
            slope = slope - dx
            if slope < 0:
                x = x + inc
                slope = slope + dy

def plot2(x,y):
    global pix
    if (x>= 0 and x<=len(pix)) and (y>= 0 and y<=len(pix[0])):
        pix[x][y] = '255 0 0'


if __name__ == "__main__":
    main()
