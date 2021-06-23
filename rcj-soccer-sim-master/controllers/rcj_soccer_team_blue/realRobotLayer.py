import math
from utilityFunctions import *

# Controlls a wheel
class Wheel:
    def __init__(self, maxSpeed, initVelocity=0, initPosition=(float('+inf'))):
        self.velocity = initVelocity
        self.position = initPosition
        self.maxSpeed = maxSpeed
    
    def setPosition(self, position):
        self.position = position
    
    def getPosition(self):
        return self.position
    
    def setVelocity(self, velocity):
        velocity = min(velocity, self.maxSpeed)
        velocity = max(velocity, self.maxSpeed * -1)
        self.velocity = velocity
        print("Wheel velocity:", self.velocity)
    
    def getVelocity(self):
        return self.velocity

# Abstraction layer for robot
class RealRobotLayer:
    def __init__(self, timeStep, name):
        # Important variables
        self.timeStep = timeStep
        self.maxSpeed = 10
        self.invertRotation = False

        # Devices
        self.rightWheel = Wheel(self.maxSpeed)
        self.leftWheel = Wheel(self.maxSpeed)

        # Identification
        self.name = name
        self.team = self.name[0]
        self.playerId = int(self.name[1])

        # Location variables
        self.rotation = 0
        self.position = [0, 0]
    
    def setRotation(self, rotation):

        """
        if rotation > math.pi / 2:
            rotation = (math.pi - rotation) * -1
        elif rotation < (math.pi / 2) * -1:
            rotation = (math.pi * -1 - rotation) * -1
        """
        self.rotation = rotation
    
    @property
    def rotationInDegs(self):
        return radsToDegs(self.rotation)

    def setPosition(self, position):
        self.position = position
    
    def moveWheels(self, ratio1, ratio2):
        ratio1 = max(min(ratio1, 1), -1)
        ratio2 = max(min(ratio2, 1), -1)
        self.rightWheel.setVelocity(ratio1 * self.maxSpeed)
        self.leftWheel.setVelocity(ratio2 * self.maxSpeed)
    

    def getDiffToDegs(self, degs):
        return self.rotationInDegs - degs
    
    def getDistToDegs(self, degs):
        return max(round(self.rotationInDegs), degs) - min(self.rotationInDegs, degs)
    
    def rotateInPlace(self, direction, speedFract):
        self.moveWheels(direction[0] * speedFract, direction[1] * speedFract)
    
    def rotateSmoothly(self, direction, speedFract, ratio):
        if direction == [-1, 1]:
            self.moveWheels(ratio * speedFract, speedFract)
        else:
            self.moveWheels(speedFract, ratio * speedFract)
    
    def moveToCoords(self, coords):
        posDiff = substractLists(self.position, coords)
        ang = getDegsFromCoords(posDiff)
        posDist = getDistance(posDiff)
        rotDist = self.getDistToDegs(ang)
        rotDiff = self.getDiffToDegs(ang)
        print("rotDiff:", rotDiff)
        print("traget ang: ", ang)
        
        if 180 > rotDiff > 0 or rotDiff < -180:
            direction = [1, -1]
        else:
            direction = [-1, 1]

        if  rotDist < 2:
            self.moveWheels(1, 1)
        elif rotDist < 5:
            self.rotateSmoothly(direction, 1, 0.9)
        elif rotDist < 15:
            self.rotateSmoothly(direction, 1, 0.8)
        else:
            self.rotateInPlace(direction, 1)

        if posDist < 0.05:
            self.moveWheels(0, 0)
            return True


