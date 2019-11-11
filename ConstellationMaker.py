import sys
import os
import turtle
from FunctionPlotter import *

# Constants defined in FunctionPlotter


# Set the screen
def setup():
    pointer = turtle.Turtle()
    screen = turtle.getscreen()
    screen.setup(WIDTH, HEIGHT, 0, 0)
    screen.setworldcoordinates(0, 0, WIDTH, HEIGHT)
    pointer.hideturtle()
    screen.delay(delay=0)
    turtle.bgcolor(BACKGROUNDCOLOR)
    pointer.up()
    return pointer


# Usage function
def usage():
    print ('To run file, use one of the following:')
    print('1. python3 ConstellationMaker.py')
    print('2. python3 ConstellationMaker.py -name')
    print('3. python3 ConstellationMaker.py -box')
    print('4. python3 ConstellationMaker.py -name -box')



# Read stars file
def readStarInformation(file):
    lines = file.readlines()
    infolist = []
    namedstars = {}
    for i in lines:
        line = i.rstrip('\n').split(",")
        info = [float(line[0]), float(line[1]), float(line[4])]
        infolist.append(info)
        if line[6] != '':
            names = line[6].split(";")
            for name in names:
                namedstars[name] = info
    return infolist, namedstars



# Draw axes
def drawAxes(pointer):
    
    # Set axes color
    pointer.color(AXISCOLOR)
    
    # Draw the axes
    drawXAxis(pointer, ORIGIN_X, ORIGIN_Y, RATIO)
    drawYAxis(pointer, ORIGIN_X, ORIGIN_Y, RATIO)



# Draw stars
def drawStars(pointer, flag, infolist, namedstars):
    
    for info in infolist:
        x, y = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, info[0], info[1])
        radius = (10 / (info[2] + 2)) / 2
        pointer.penup()
        pointer.goto(x, y - radius)
        pointer.color(STARCOLOR2)
        pointer.pendown()
        pointer.begin_fill()
        # Draw circle
        pointer.circle(radius)
        pointer.end_fill()
    
    for key, value in namedstars.items():
        x, y = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, value[0], value[1])
        radius = (10 / (value[2] + 2)) / 2
        pointer.penup()
        pointer.goto(x, y - radius)
        pointer.color(STARCOLOR)
        pointer.pendown()
        pointer.begin_fill()
        # Draw circle
        pointer.circle(radius)
        pointer.end_fill()
        if flag == 1:
            pointer.write(key,font=("Arial", 5, "normal"))



# Read constellation
def readConstellation(file):
    lines = file.readlines()
    constellationName = lines[0]
    lines.pop(0)
    
    edges = []
    for i in lines:
        line = i.rstrip('\n').split(",")
        edges.append([line[0], line[1]])
    
    # Create a temporary list of distinct stars from file
    temp = []
    for i in edges:
        for j in i:
            if j not in temp:
                temp.append(j)
    return constellationName, edges, temp



# Draw constellation
def drawConstellation (pointer, infolist, namedstars, constellationName, edges, counter):
    
    pointer.color(getColor(counter))
    for edge in edges:
        x1, y1 = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, namedstars[edge[0]][0], namedstars[edge[0]][1])
        x2, y2 = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, namedstars[edge[1]][0], namedstars[edge[1]][1])
        pointer.penup()
        pointer.goto(x1, y1)
        pointer.pendown()
        pointer.goto(x2, y2)



# Draw box around the constellations
def drawBox(pointer, constellationname, namedstars, starlist):
    
    # Iterate through x and y coordinates of all constellation stars to find min and max x,y values and convert them to pixels
    xlist = [namedstars[star][0] for star in starlist]
    ylist = [namedstars[star][1] for star in starlist]
    xmin, xminy = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, min(xlist), ylist[xlist.index(min(xlist))])
    xmax, xmaxy = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, max(xlist), ylist[xlist.index(max(xlist))])
    ymin, yminy = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, min(ylist), xlist[ylist.index(min(ylist))])
    ymax, ymaxy = screenCoor(ORIGIN_X, ORIGIN_Y, RATIO, max(ylist), xlist[ylist.index(max(ylist))])
    
    # Add pad to xmin, xmax, ymin and ymax
    xmin -= PAD
    xmax += PAD
    ymin -= PAD
    ymax += PAD
    
    # Draw box
    pointer.penup()
    pointer.color(BOXCOLOR)
    pointer.goto(xmin, xminy)
    pointer.pendown()
    pointer.goto(xmin, ymax)
    pointer.goto(xmax, ymax)
    pointer.goto(xmax, ymin)
    pointer.goto(xmin, ymin)
    pointer.goto(xmin, ymax)
    
    # Write constellation name above box
    pointer.penup()
    pointer.goto(xmin, ymax + TEXTPAD)
    pointer.write(constellationname,font=("Arial", 5, "normal"))



def main():
    nameflag = 0
    boxflag = 0
    
    # Handle arguments
    if len(sys.argv) == 1:
        pass
    
    elif len(sys.argv) == 2 and sys.argv[1] == '-name':
        nameflag = 1

    elif len(sys.argv) == 2 and sys.argv[1] == '-box':
        boxflag = 1

    elif len(sys.argv) == 3 and sys.argv[1] == '-name' and sys.argv[2] == '-box':
        nameflag = 1
        boxflag = 1

    else:
        print ('Error! Check arguments')
        sys.exit()


    # Open stars file
    filename = 'stars_list.dat'
    file = open(filename, 'r')

    # Read star information from file
    infolist, namedstars = readStarInformation(file)

    # Close file
    file.close()

    # Set up the drawing board
    pointer = setup()

    # Draw axes
    drawAxes(pointer)

    # Draw stars
    drawStars(pointer, nameflag, infolist, namedstars)

    # Loop getting filenames
    with open('constellations_list.dat', 'r') as file:
        counter = 0
        for cfilename in file:
            
            # Strip newline character from filename
            cfilename = cfilename.strip()

            # Open stars file
            file = open('constellations/' + cfilename, 'r')
            
            # Read constellation file
            constellationName, edges, starlist = readConstellation(file)

            # Draw Constellation
            drawConstellation(pointer, infolist, namedstars, constellationName, edges, counter)
            
            # Draw bounding box
            if boxflag == 1:
                drawBox(pointer, constellationName, namedstars, starlist)
            
            # Increment counter
            counter += 1

    # Close file
    file.close()

    # Exit on click
    turtle.done()

main()
