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
        elif cache[0] == 'sphere':
            sphere(edge,cache[1:])
        elif cache[0] == 'pixels':
            for x in range(int(cache[1])):
                pix.append([])
                for y in range(int(cache[2])):
                    pix[x].append('0 0 0')
        elif cache[0] == 'transform':
            edge = multiM(trans,edge)
        elif cache[0] == 'render-parallel':
            draw(edge)
        elif cache[0] == 'render-perspective-cyclops':
            draw(edge,cache[1],cache[2],cache[3])
        elif cache[0] == 'render-perspective-stereo':
            draw(edge,cache[1],cache[2],cache[3],cache[4],cache[5],cache[6])
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

def sphere(m,p):
    tmp = createM(0)
    tmp2 = []
    r = p[0]
    x = p[1]
    y = p[2]
    z = p[3]
    a = (2*math.pi)/20
    for phi in range(0,11):
        for the in range(0,21):
            addCol(tmp)
            setM(tmp,len(tmp)-1,0,x+(r*sin(the*a)*cos(phi*a)))
            setM(tmp,len(tmp)-1,1,y+(r*sin(the*a)*sin(phi*a)))
            setM(tmp,len(tmp)-1,2,z+(r*cos(the*a)))
            setM(tmp,len(tmp)-1,3,1)
            if (the != 0 and the != 20):
                addCol(tmp)
                setM(tmp,len(tmp)-1,0,x+(r*sin(the*a)*cos(phi*a)))
                setM(tmp,len(tmp)-1,1,y+(r*sin(the*a)*sin(phi*a)))
                setM(tmp,len(tmp)-1,2,z+(r*cos(the*a)))
                setM(tmp,len(tmp)-1,3,1)
        if (the != 0):
            for j in range(0,21):
                tmp2.append(tmp[((phi-1)*40) + j])
                tmp2.append(tmp[((phi)*40) + j])
    for i in tmp:
        m.append(i)
    for i in tmp2:
        m.append(i)
            
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

def drawLine(A,B,C,D,c='255 255 255'):
    x1 = A
    y1 = B
    x2 = C
    y2 = D
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    global pix    
    if (dx==0 and dy==0):
        plot(x1,y1,c)
    elif (dy==0):
        
        for x in range(min(x1,x2+1),max(x1,x2+1)):
            plot(x,y1,c)
    elif (dx == 0):        
        for y in range(min(y1,y2+1),max(y1,y2+1)):
            plot(x1,y,c)            
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
            plot(x,y,c)
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
            plot(x,y,c)
            slope = slope - dx
            if slope < 0:
                x = x + inc
                slope = slope + dy


def plot(x,y,c):
    global pix
    if (x>= 0 and x<=len(pix)) and (y>= 0 and y<=len(pix[0])):
        pix[x][y] = c

def draw(m,x1='d',y1='d',z1='d',x2='d',y2='d',z2='d'):
    i = 0
    xl,yb,xr,yt = screen
    pxl,pxr,pyt,pyb = 0,len(pix),0,len(pix[0])
    while(i+1<len(m)): 
        if not x1 == 'd':
            A = ( ( (m[i][0]-x1) *(0-z1) )/(m[i][2]-z1) )+x1
            B = ( ( (m[i][1]-y1) *(0-z1) )/(m[i][2]-z1) )+y1
            C = ( ( (m[i+1][0]-x1) *(0-z1) )/(m[i+1][2]-z1) )+x1
            D = ( ( (m[i+1][1]-y1) *(0-z1) )/(m[i+1][2]-z1) )+y1
            A = ( ( (A-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            B = ( ( (B-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            C = ( ( (C-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            D = ( ( (D-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            if not x2 == 'd':
                drawLine(int(A),int(B),int(C),int(D),'255 0 0')
                A = ( ( (m[i][0]-x2) *(0-z2) )/(m[i][2]-z2) )+x2
                B = ( ( (m[i][1]-y2) *(0-z2) )/(m[i][2]-z2) )+y2
                C = ( ( (m[i+1][0]-x2) *(0-z2) )/(m[i+1][2]-z2) )+x2
                D = ( ( (m[i+1][1]-y2) *(0-z2) )/(m[i+1][2]-z2) )+y2
                A = ( ( (A-xl)*(pxr-pxl) )/(xr-xl) )+pxl
                B = ( ( (B-yb)*(pyt-pyb) )/(yt-yb) )+pyb
                C = ( ( (C-xl)*(pxr-pxl) )/(xr-xl) )+pxl
                D = ( ( (D-yb)*(pyt-pyb) )/(yt-yb) )+pyb
                drawLine(int(A),int(B),int(C),int(D),'0 255 255')
        else:
            A = ( ( (m[i][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            B = ( ( (m[i][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            C = ( ( (m[i+1][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            D = ( ( (m[i+1][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
        if x2 == 'd':
            drawLine(int(A),int(B),int(C),int(D))            
        i = i + 2

if __name__ == "__main__":
    main()
