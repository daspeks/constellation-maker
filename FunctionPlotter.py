from math import *

WIDTH           = 600
HEIGHT          = 600
RATIO           = 300
ORIGIN_X        = 300 # Pixel coordinates
ORIGIN_Y        = 300
XORIGIN         = 0   # Cartesian coordinates
YORIGIN         = 0
XMIN            = -1
YMIN            = -1
XMAX            = 1
YMAX            = 1
TICKSIZE        = 5
PAD             = 15
TEXTPAD         = 2
LABELOFFSET     = 20
STEP            = 0.25
AXISCOLOR       = "blue"
BOXCOLOR        = "orange"
BACKGROUNDCOLOR = "black"
STARCOLOR       = "white"
STARCOLOR2      = "grey"


# Returns pixel coordinates of corresponding Cartesian coordinates
def screenCoor(xorigin, yorigin, ratio, x, y):
    screenX = xorigin + (ratio * x)
    screenY = yorigin + (ratio * y)
    return screenX, screenY


# Maps expression color based on counter
def getColor(counter):
    if ((counter % 3) == 0):
        return "red"
    elif ((counter % 3) == 1):
        return "green"
    else:
        return "yellow"


# Draws the X-axis ticks and labels on screen
def drawXAxisLabelTick(pointer, screenX, screenY, text):
    pointer.goto(screenX, screenY + TICKSIZE)
    pointer.down()
    pointer.goto(screenX, screenY - TICKSIZE)
    pointer.up()
    pointer.goto(screenX, screenY - LABELOFFSET)
    pointer.write(text, False, align = 'center')


# Draws the Y-axis ticks and labels on screen
def drawYAxisLabelTick(pointer, screenX, screenY, text):
    pointer.goto(screenX + TICKSIZE, screenY)
    pointer.down()
    pointer.goto(screenX - TICKSIZE, screenY)
    pointer.up()
    pointer.goto(screenX - LABELOFFSET, screenY)
    pointer.write(text, False, align = 'center')


# Draws the X-axis on screen
def drawXAxis(pointer, xorigin, yorigin, ratio):
    list = [-STEP, STEP]
    for step in list:
        screenX = xorigin
        screenY = yorigin
        pointer.up()
        pointer.goto(screenX, screenY)
        
        x = step
        condition = (XMIN <= x <= XMAX)
        while (condition):
            screenX, screenY = screenCoor(xorigin, yorigin, ratio, x, YORIGIN)
            pointer.down()
            pointer.goto(screenX, screenY)
            pointer.up()
            drawXAxisLabelTick(pointer, screenX, screenY, str(x))
            pointer.goto(screenX, screenY)
            pointer.down()
            x = x + step
            condition = (XMIN <= x <= XMAX)

    pointer.up()



# Draws the Y-axis on screen
def drawYAxis(pointer, xorigin, yorigin, ratio):
    ymin = 0
    ymax = 0
    list = [-STEP, STEP]
    for step in list:
        screenX = xorigin
        screenY = yorigin
        pointer.up()
        pointer.goto(screenX, screenY)
        
        y = step
        condition = (YMIN <= y <= YMAX)
        while (condition):
            screenX, screenY = screenCoor(xorigin, yorigin, ratio, XORIGIN, y)
            pointer.down()
            pointer.goto(screenX, screenY)
            pointer.up()
            drawYAxisLabelTick(pointer, screenX, screenY, str(y))
            pointer.goto(screenX, screenY)
            pointer.down()
            y = y + step
            condition = (YMIN <= y <= YMAX)

    pointer.up()
    return ymin, ymax
