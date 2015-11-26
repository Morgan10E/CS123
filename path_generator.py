#This file will contain code for taking in an image and returning a queue of paths for the robot to follow
# PLEASE TAKE CARE - EVERYTHING IS IN COORDINATES (ROW,COLUMN) --> IN OTHER WORDS, (Y,X)
from PIL import Image
import Queue
import numpy
import copy

DARK_VAL = 150
UP = (-1,0)
RIGHT = (0,1)
DOWN = (1,0)
LEFT = (0,-1)
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
            array[r][c] = pixelList[r*width + c]
    return array

def printPixelArray(array):
    for r in range(0, len(array)):
        row = ""
        for c in range(0, len(array[r])):
            row = row + str(array[r][c]) + " "
        print row

def print01Array(array):
    for r in range(0, len(array)):
        row = ""
        for c in range(0, len(array[r])):
            if array[r][c]:
                row = row + "1 "
            else:
                row = row + "0 "
        print row

def printBlackEnoughArray(array):
    for r in range(0, len(array)):
        row = ""
        for c in range(0, len(array[r])):
            if isBlackEnough(array[r][c]):
                row = row+" 1"
            else:
                row = row+" 0"
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
    allPaths = []
    height = len(array)
    width = len(array[0])
    for r in range(0, height):
        for c in range(0, width):
            if len(allPaths) > 25:
                return allPaths
            if array[r][c]:
                print "Getting path " + str(len(allPaths) + 1)
                vec = []
                vec.append(((r,c),(r+1,c)))
                getNextStep((r+1, c), (r, c), array, vec)
                allPaths.append(vec)
                mask = getInversionMask(vec, array)
                # printPixelArray(mask)
                invertForMask(array, mask)
                # print01Array(array)
                r = 0
                c = 0
    return allPaths

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
        # print "Turning Right"
        if direction == UP:
            nextPoint = tuple(numpy.add(current, (0,1)))
        if direction == RIGHT:
            nextPoint = tuple(numpy.add(current, (1,0)))
        if direction == DOWN:
            nextPoint = tuple(numpy.add(current, (0,-1)))
        if direction == LEFT:
            nextPoint = tuple(numpy.add(current, (-1,0)))
    elif (square == GO_STRAIGHT):
        # print "Going Straight"
        nextPoint = tuple(numpy.add(current, direction))
    else:
        # go left
        # print "Going Left"
        if direction == UP:
            nextPoint = tuple(numpy.add(current, (0,-1)))
        if direction == RIGHT:
            nextPoint = tuple(numpy.add(current, (-1,0)))
        if direction == DOWN:
            nextPoint = tuple(numpy.add(current, (0,1)))
        if direction == LEFT:
            nextPoint = tuple(numpy.add(current, (1,0)))
    vec.append((current, nextPoint))
    getNextStep(nextPoint,start,array,vec)

# rotates 90 degrees to the right
def rotated(array):
    return tuple(zip(*array[::-1]))

#orients it to always act as if our direction is 'up' for comparison to TURN_RIGHT/GO_STRAIGHT
def getSurroundingSquare((r,c), array, direction):
    square = ((array[r-1][c-1], array[r-1][c]),(array[r][c-1], array[r][c]))
    if direction == UP:
        return square
    square = rotated(square)
    if direction == LEFT:
        return square
    square = rotated(square)
    if direction == DOWN:
        return square
    return rotated(square)

def getDirection(edge):
    return tuple(numpy.subtract(edge[1],edge[0]))

def getInversionMask(path, array):
    height = len(array)
    width = len(array[0])
    mask = [[0 for x in range(0,width)] for x in range(0,height)]
    for edge in path:
        direction = getDirection(edge)
        if direction == DOWN:
            mask[edge[0][0]][edge[0][1]] = 1
        elif direction == LEFT:
            mask[edge[1][0]][edge[1][1]] = 1
        elif direction == UP:
            mask[edge[1][0]][edge[1][1] - 1] = 1
        else:
            mask[edge[0][0] - 1][edge[0][1]] = 1
    firstEdge = path[0]
    secondEdge = path[1]
    secondDir = getDirection(secondEdge)

    outline = copy.deepcopy(mask)

    floodFill(mask, tuple(numpy.add(firstEdge[1], (-1,-1))))
    # printPixelArray(mask)

    for r in range(0, height):
        for c in range(0, width):
            if outline[r][c] == 1:
                mask[r][c] = 1
    # printPixelArray(mask)

    return mask

def floodFill(mask, loc):
    height = len(mask)
    width = len(mask[0])
    q = Queue.Queue()
    q.put(loc)
    while not q.empty():
        loc = q.get()
        if loc[0] < 0 or loc[1] < 0 or loc[0] >= height or loc[1] >= width or mask[loc[0]][loc[1]] == 1:
            continue
        mask[loc[0]][loc[1]] = 1
        q.put(tuple(numpy.add(loc, UP)))
        q.put(tuple(numpy.add(loc, RIGHT)))
        q.put(tuple(numpy.add(loc, LEFT)))
        q.put(tuple(numpy.add(loc, DOWN)))
    if mask[0][0] == 1:
        for r in range(0, height):
            for c in range(0, width):
                if mask[r][c] == 1:
                    mask[r][c] = 0
                else:
                    mask[r][c] = 1
    # if mask[loc[0]][loc[1]] == 1:
    #     return
    # mask[loc[0]][loc[1]] = 1
    # floodFill(mask, tuple(numpy.add(loc, UP)))
    # floodFill(mask, tuple(numpy.add(loc, RIGHT)))
    # floodFill(mask, tuple(numpy.add(loc, LEFT)))
    # floodFill(mask, tuple(numpy.add(loc, DOWN)))

def invertForMask(array, mask):
    height = len(array)
    width = len(array[0])
    for r in range(0, height):
        for c in range(0, width):
            if mask[r][c] == 1:
                array[r][c] = not array[r][c]
