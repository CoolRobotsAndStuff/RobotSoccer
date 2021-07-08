import math
from angles import Angle

# Corrects the given angle in degrees to be in a range from 0 to 360
def normalizeAng(ang):
    ang.d = ang.d % 360
    if ang.d < 0:
        ang.d += 360
    if ang.d == 360:
        ang.d = 0
    return ang

# Converts a number from a range of value to another
def mapVals(val, in_min, in_max, out_min, out_max):
    return (val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

# Gets x, y coordinates from a given angle in radians and distance
def getCoordsFromAng(ang, distance):
    y = float(distance * math.cos(ang.r))
    x = float(distance * math.sin(ang.r))
    return [x, y]

def getAngFromCoords(coords):
    return Angle(r=math.atan2(coords[0], coords[1]))

# Gets the distance to given coordinates
def getDistance(position):
    return math.sqrt((position[0] ** 2) + (position[1] ** 2))

# Checks if a value is between two values
def isInRange(val, minVal, maxVal):
    return minVal < val < maxVal


def multiplyLists(list1, list2):
    finalList = []
    for item1, item2 in zip(list1, list2):
        finalList.append(item1 * item2)
    return finalList

def sumLists(list1, list2):
    finalList = []
    for item1, item2 in zip(list1, list2):
        finalList.append(item1 + item2)
    return finalList

def substractLists(list1, list2):
    finalList = []
    for item1, item2 in zip(list1, list2):
        finalList.append(item1 - item2)
    return finalList

def divideLists(list1, list2):
    finalList = []
    for item1, item2 in zip(list1, list2):
        finalList.append(item1 / item2)
    return finalList