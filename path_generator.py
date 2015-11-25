#This file will contain code for taking in an image and returning a queue of paths for the robot to follow
# PLEASE TAKE CARE - EVERYTHING IS IN COORDINATES (ROW,COLUMN) --> IN OTHER WORDS, (Y,X)
from PIL import Image
import Queue
import numpy

DARK_VAL = 150
NORTH = (-1,0)
EAST = (0,1)
SOUTH = (1,0)
WEST = (0,-1)
TURN_RIGHT = ((True, True),(True, False))
GO_STRAIGHT = ((True, False),(True, False))


def getPixelArrayForFilename(filename):
    image = Image.open(filename, 'r')
    if (not image):
        print "bad filename"
        return
    pixelList = list(image.getdata())
    width = image.size[0]
    height = image.size[1]
    array = [[0 for x in range(0,width)] for x in range(0,height)]
    for r in range(0, height):
        for c in range(0, width):
            array[r][c] = pixelList[r*height + c]
    return array

def printPixelArray(array):
    for r in range(0, len(array)):
        row = ""
        for c in range(0, len(array[r])):
            row = row + str(array[r][c]) + " "
        print row

def printBlackEnoughArray(array):
    for r in range(0, len(array)):
        row = ""
        for c in range(0, len(array[r])):
            if isBlackEnough(array[r][c]):
                row = row+"1"
            else:
                row = row+"0"
        print row

def isBlackEnough(pixel):
    return pixel[0] < DARK_VAL and pixel[1] < DARK_VAL and pixel[2] < DARK_VAL

def getBoolArray(array):
    height = len(array)
    width = len(array[0])
    boolArray = [[0 for x in range(0,width)] for x in range(0,height)]
    for r in range(0, height):
        for c in range(0, width):
            boolArray[r][c] = isBlackEnough(array[r][c])
    return boolArray

def getRawPaths(array):
    vec = []
    height = len(array)
    width = len(array[0])
    for r in range(0, height):
        for c in range(0, width):
            if array[r][c]:
                vec.append(((r,c),(r+1,c)))
                getNextStep((r+1, c), (r, c), array, vec)
                return vec #NEED TO INVERT CONTENTS AND CONTINUE, NOT RETURN RIGHT AWAY
    return vec

def getNextStep(current, start, array, vec):
    # print vec
    if current == start:
        return
    lastEdge = vec[len(vec)-1]
    direction = tuple(numpy.subtract(lastEdge[1],lastEdge[0]))
    square = getSurroundingSquare(lastEdge[1], array, direction)
    # print printPixelArray(square)
    if (square == TURN_RIGHT):
        # turn right
        print "Turning Right"
        if direction == NORTH:
            nextPoint = tuple(numpy.add(current, (0,1)))
        if direction == EAST:
            nextPoint = tuple(numpy.add(current, (1,0)))
        if direction == SOUTH:
            nextPoint = tuple(numpy.add(current, (0,-1)))
        if direction == WEST:
            nextPoint = tuple(numpy.add(current, (-1,0)))
    elif (square == GO_STRAIGHT):
        print "Going Straight"
        nextPoint = tuple(numpy.add(current, direction))
    else:
        # go left
        print "Going Left"
        if direction == NORTH:
            nextPoint = tuple(numpy.add(current, (0,-1)))
        if direction == EAST:
            nextPoint = tuple(numpy.add(current, (-1,0)))
        if direction == SOUTH:
            nextPoint = tuple(numpy.add(current, (0,1)))
        if direction == WEST:
            nextPoint = tuple(numpy.add(current, (1,0)))
    vec.append((current, nextPoint))
    getNextStep(nextPoint,start,array,vec)

def rotated(array):
    return tuple(zip(*array[::-1]))

#orients it to always act as if our direction is 'up' for comparison to TURN_RIGHT/GO_STRAIGHT
def getSurroundingSquare((r,c), array, direction):
    square = ((array[r-1][c-1], array[r-1][c]),(array[r][c-1], array[r][c]))
    if direction == NORTH:
        return square
    square = rotated(square)
    if direction == WEST:
        return square
    square = rotated(square)
    if direction == SOUTH:
        return square
    return rotated(square)
