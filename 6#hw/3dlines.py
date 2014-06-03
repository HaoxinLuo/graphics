from matrix import *
from math import cos,sin,radians
import sys, math

edge = createM(0)
trans = idenM()
save = {}
files = {}
screen = []
pix = []
vari = {}
frames = []

def main():
    if(len(sys.argv)<2):
        print("no file name given")
        exit(0)
    f = open(sys.argv[1],'r')
    global trans,edge,screen,pix,save
    catchVary(f)
    while(True):                  
        cache = f.readline().split()        
        cache[1:]=[float(q) if isFloat(q) else vari[q][0] if q in vari else q for q in cache[1:]]
        if len(cache) < 1:
            pass
        elif cache[0] == '#' or cache[0][0] == '#':
            pass
        elif cache[0] == 'identity':
            trans = idenM()
        elif cache[0] == 'move':
            trans = multiM(move(cache[1],cache[2],cache[3]),trans)
        elif cache[0] == 'scale':
            trans = multiM(scale(cache[1],cache[2],cache[3]),trans)
        elif cache[0] == 'rotate-x':
            trans = multiM(rotate(cache[1],0),trans)
        elif cache[0] == 'rotate-y':
            trans = multiM(rotate(cache[1],1),trans)
        elif cache[0] == 'rotate-z':
            trans = multiM(rotate(cache[1],2),trans)
        elif cache[0] == 'screen':
            screen = cache[1:]
        elif cache[0] == 'pixels':
            for x in range(int(cache[1])):
                pix.append([])
                for y in range(int(cache[2])):
                    pix[x].append('0 0 0')
        ######################################################
        elif cache[0] == 'sphere-t':
            render_sphere_t(cache[1:])
        elif cache[0] == 'box-t':
            render_box_t(cache[1:])
        elif cache[0] == 'save':
            save[cache[1]] = copyM(trans)
            trans = idenM()
        elif cache[0]  == 'load':
            trans = copyM(save[cache[1]])
        ######################################################
        elif cache[0] == 'render-parallel':
            draw(edge)
        elif cache[0] == 'render-perspective-cyclops':
            draw(edge,cache[1],cache[2],cache[3])
        elif cache[0] == 'render-perspective-stereo':
            draw(edge,cache[1],cache[2],cache[3],cache[4],cache[5],cache[6])
        elif cache[0] == 'clear-triangles':
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
        ######################################################
        elif cache[0] == 'files':
            if cache[1] not in files:
                files[cache[1]] = str(frames[0]-1)
            files[cache[1]] = str(int(files[cache[1]])+1).zfill(3)
            n = open(cache[1]+files[cache[1]]+".ppm",'w')
            n.write("P3\n "+str(len(pix))+' '+str(len(pix[0]))+"\n 255\n")
            for y in range(len(pix[0])):
                for x in range(len(pix)):
                    n.write(pix[x][y] + ' ') 
            if int(files[cache[1]]) < frames[1]:
                f.seek(0)
                pix = []
                edge = createM(0)
                trans = idenM()
                save = {}
                screen = []                
                for v in vari:
                    for i in range(len(vari[v])/4):
                        lower = vari[v][2+(i*4)]
                        upper = vari[v][3+(i*4)]
                        cframe = int(files[cache[1]])
                        if (cframe >= lower and cframe <= upper):
                            vari[v][0] = vari[v][i*4] + (cframe*vari[v][1+(i*4)])
        ########################################################
        elif cache[0] == 'end':
            break
        else:
            pass

def applyTrans(m):
    global trans
    i = len(stack)-1
    while i >= 0:
        trans = stack[i]
        m = multiM(trans,m)
        i= i - 1
    return m

def uSphere():
    tmp = createM(0)
    a = (math.pi)/10
    for phi in range(0,21):
        for the in range(0,11):
            addCol(tmp)
            setM(tmp,len(tmp)-1,0,sin(the*a)*cos(phi*a))
            setM(tmp,len(tmp)-1,1,sin(the*a)*sin(phi*a))
            setM(tmp,len(tmp)-1,2,-cos(the*a))
            setM(tmp,len(tmp)-1,3,1)
    return tmp

def uBox():
    tmp = createM(0)
    tmp.append([-.5,.5,.5,1])
    tmp.append([-.5,-.5,.5,1])
    tmp.append([.5,-.5,.5,1])
    tmp.append([.5,.5,.5,1])
    tmp.append([-.5,.5,-.5,1])
    tmp.append([-.5,-.5,-.5,1])
    tmp.append([.5,-.5,-.5,1])
    tmp.append([.5,.5,-.5,1])
    return tmp


def render_sphere_t(p):
    global edge
    pts = uSphere()
    tmp = createM(0)
    trigen_sphere(tmp,pts)   
    lT = idenM()
    s= scale(p[0],p[1],p[2])
    rx = rotate(p[3],0)
    ry = rotate(p[4],1)
    rz = rotate(p[5],2)
    m = move(p[6],p[7],p[8])
    lT = multiM(s,lT)
    lT = multiM(rx,lT)
    lT = multiM(ry,lT)
    lT = multiM(rz,lT)
    lT = multiM(m,lT)
    tmp = multiM(lT,tmp)
    tmp = multiM(trans,tmp)
    for i in tmp:
        edge.append(i)

def trigen_sphere(m,pts):
    a = 11
    b = 12
    c = 0
    i = 0
    j = len(pts) -1
    while a < j:
        if ((c+1)%11 != 0):
            m.append(pts[a])
            m.append(pts[b])
            m.append(pts[c])
        i = i + 1
        if (i%2 != 0):
            a = a + 1
            b = a - 11
        else:
            b = b + 12
            c = c + 1

def render_box_t(p):
    global edge
    pts = uBox()
    tmp = createM(0)
    tmp = trigen_cube(pts)
    lT = idenM()
    s= scale(p[0],p[1],p[2])
    rx = rotate(p[3],0)
    ry = rotate(p[4],1)
    rz = rotate(p[5],2)
    m = move(p[6],p[7],p[8])
    lT = multiM(s,lT)
    lT = multiM(rx,lT)
    lT = multiM(ry,lT)
    lT = multiM(rz,lT)
    lT = multiM(m,lT)
    tmp = multiM(lT,tmp)
    tmp = multiM(trans,tmp)
    for i in tmp:
        edge.append(i)

def trigen_cube(pts):
    m = []
    m.append(pts[0]) #front
    m.append(pts[1])
    m.append(pts[3])
    m.append(pts[1])
    m.append(pts[2])
    m.append(pts[3])
        
    m.append(pts[7]) #back
    m.append(pts[6])
    m.append(pts[4])
    m.append(pts[6])
    m.append(pts[5])
    m.append(pts[4])
    
    m.append(pts[3]) #right
    m.append(pts[2])
    m.append(pts[7])
    m.append(pts[2])
    m.append(pts[6])
    m.append(pts[7])
    
    m.append(pts[4]) #left
    m.append(pts[1])
    m.append(pts[0])
    m.append(pts[1])
    m.append(pts[4])
    m.append(pts[5])
    
    m.append(pts[4]) #top
    m.append(pts[0])
    m.append(pts[7])
    m.append(pts[0])
    m.append(pts[3])
    m.append(pts[7])
    
    m.append(pts[1]) #bottom
    m.append(pts[6])
    m.append(pts[2])
    m.append(pts[1])
    m.append(pts[5])
    m.append(pts[6])
    return m

def move(x,y,z):
    tmp = idenM()
    setM(tmp,3,0,x)
    setM(tmp,3,1,y)
    setM(tmp,3,2,z)
#    trans = multiM(tmp,trans)
    return tmp

def scale(x,y,z):
    tmp = idenM()
    setM(tmp,0,0,x)
    setM(tmp,1,1,y)
    setM(tmp,2,2,z)
#    trans = multiM(tmp,trans)
    return tmp

def rotate(a,d):
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
#    trans = multiM(tmp,trans)
    return tmp

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
    if (x>= 0 and x<len(pix)) and (y>= 0 and y<len(pix[0])):
        pix[x][y] = c

def draw(m,x1='d',y1='d',z1='d',x2='d',y2='d',z2='d'):
    i = 0
    xl,yb,xr,yt = screen
    pxl,pxr,pyt,pyb = 0,len(pix),0,len(pix[0])
    while(i+2<len(m)):
        if not x1 == 'd':
            A = ( ( (m[i][0]-x1) *(0-z1) )/(m[i][2]-z1) )+x1
            B = ( ( (m[i][1]-y1) *(0-z1) )/(m[i][2]-z1) )+y1
            C = ( ( (m[i+1][0]-x1) *(0-z1) )/(m[i+1][2]-z1) )+x1
            D = ( ( (m[i+1][1]-y1) *(0-z1) )/(m[i+1][2]-z1) )+y1
            E = ( ( (m[i+2][0]-x1) *(0-z1) )/(m[i+2][2]-z1) )+x1
            F = ( ( (m[i+2][1]-y1) *(0-z1) )/(m[i+2][2]-z1) )+y1
            A = ( ( (A-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            B = ( ( (B-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            C = ( ( (C-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            D = ( ( (D-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            E = ( ( (E-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            F = ( ( (F-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            if not x2 == 'd':
                if cull(m[i],m[i+1],m[i+2],[x1,y1,z1]):
                    drawLine(int(A),int(B),int(C),int(D),'255 0 0')
                    drawLine(int(A),int(B),int(E),int(F),'255 0 0')
                    drawLine(int(C),int(D),int(E),int(F),'255 0 0')
                A = ( ( (m[i][0]-x2) *(0-z2) )/(m[i][2]-z2) )+x2
                B = ( ( (m[i][1]-y2) *(0-z2) )/(m[i][2]-z2) )+y2
                C = ( ( (m[i+1][0]-x2) *(0-z2) )/(m[i+1][2]-z2) )+x2
                D = ( ( (m[i+1][1]-y2) *(0-z2) )/(m[i+1][2]-z2) )+y2
                E = ( ( (m[i+2][0]-x2) *(0-z2) )/(m[i+2][2]-z2) )+x2
                F = ( ( (m[i+2][1]-y2) *(0-z2) )/(m[i+2][2]-z2) )+y2
                A = ( ( (A-xl)*(pxr-pxl) )/(xr-xl) )+pxl
                B = ( ( (B-yb)*(pyt-pyb) )/(yt-yb) )+pyb
                C = ( ( (C-xl)*(pxr-pxl) )/(xr-xl) )+pxl
                D = ( ( (D-yb)*(pyt-pyb) )/(yt-yb) )+pyb
                E = ( ( (E-xl)*(pxr-pxl) )/(xr-xl) )+pxl
                F = ( ( (F-yb)*(pyt-pyb) )/(yt-yb) )+pyb         
                if cull(m[i],m[i+1],m[i+2],[x2,y2,z2]):
                    drawLine(int(A),int(B),int(C),int(D),'0 255 255')
                    drawLine(int(A),int(B),int(E),int(F),'0 255 255')
                    drawLine(int(C),int(D),int(E),int(F),'0 255 255')
        else:
            A = ( ( (m[i][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            B = ( ( (m[i][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            C = ( ( (m[i+1][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            D = ( ( (m[i+1][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            E = ( ( (m[i+2][0]-xl)*(pxr-pxl) )/(xr-xl) )+pxl
            F = ( ( (m[i+2][1]-yb)*(pyt-pyb) )/(yt-yb) )+pyb
            
        if x2 == 'd':
            if cull(m[i],m[i+1],m[i+2],[x1,y1,z1]):
                drawLine(int(A),int(B),int(C),int(D))            
                drawLine(int(A),int(B),int(E),int(F))            
                drawLine(int(C),int(D),int(E),int(F))            
        i = i + 3

def cull(*args):
    p1 = args[0]
    p2 = args[1]
    p3 = args[2]
    if args[3][0] != 'd':
        e = args[3]
    else:
        e = [0,0,4]
    s = [[p1[0]-e[0],p1[1]-e[1],p1[2]-e[2]]]
    t1 = [[p2[0]-p1[0],p2[1]-p1[1],p2[2]-p1[2]]]
    t2 = [[p3[0]-p2[0],p3[1]-p2[1],p3[2]-p2[2]]]

    c = crossP(t1[0],t2[0])
    d = dotP(s[0],c[0])
    return d < 0

######################################HW#6###################################

def isFloat(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return True
    
def catchVary(n):
    global frames,vari
    while(True):
        cache = n.readline().split()
        cache[1:]=[float(q) if isFloat(q) else q for q in cache[1:]]
        if len(cache) < 1:
            pass
        elif cache[0] == "vary":
            if cache[1] not in vari:
                vari[cache[1]] = [cache[2],(cache[3]-cache[2])/(cache[5]-cache[4]),cache[4],cache[5]]
            else:
                vari[cache[1]]=vari[cache[1]]+[cache[2],(cache[3]-cache[2])/(cache[5]-cache[4]),cache[4],cache[5]]
        elif cache[0] == "frames":
            frames = [int(cache[1]),int(cache[2])]
        elif cache[0] == "end":
            n.seek(0)
            break
        else:
            pass


if __name__ == "__main__":
    main()
