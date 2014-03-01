import sys
import math

screen = []
for x in range(500):
    screen.append([])
    for y in range(500):
        screen[x].append("0 0 0")
c = "0 0 0"
def main():
    if(len(sys.argv)<2):
        print("no file name given\n")
        exit(0)
    f = open(sys.argv[1],'r')
    global c
    mode = ""
    while(True):
        mode = f.readline().strip()
        if (mode == 'c'):
            c = f.readline().strip()
        elif (mode == '#'):
            f.readline()
        elif (mode == 'g'):
            n = open(f.readline().strip(),'w')
            n.write("P3\n 500 500\n 255\n")
            for y in range(500):
                for x in range(500):
                    n.write(screen[y][x])
                    n.write(" ")
        elif (mode == 'q'):
            f.close()
            n.close()            
            exit(0)
        elif (mode == 'l'):
            mode = f.readline().strip()
            mode = [int(x) for x in mode.split()]
            drawLine(mode[0],mode[1],mode[2],mode[3])

def drawLine(A,B,C,D):
    x1 = A
    x2 = C
    y1 = B
    y2 = D
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    global screen
    
    if (dx==0 and dy==0):
        plot(y1,x1)
    elif (dy==0):
        for x in range(x1,x2+1):
            plot(y1,x)
    elif (dx == 0):
        for y in range(y1,y2+1):
            plot(y,x1)
            
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
            plot(y,x)
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
            plot(y,x)
            slope = slope - dx
            if slope < 0:
                x = x + inc
                slope = slope + dy

def plot(y,x):
    global screen
    screen[y][x] = c
#    print(x,y)



if __name__ == "__main__":
    main()

