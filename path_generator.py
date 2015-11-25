#This file will contain code for taking in an image and returning a queue of paths for the robot to follow
from PIL import Image

DARK_VAL = 150

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
