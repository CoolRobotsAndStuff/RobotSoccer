import math
from UtilityFunctions import *
from angles import Angle

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
class RobotModell:
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
        self.rotation = Angle(r=0)
        self.position = [0, 0]
    
    def setRotation(self, rotation):
        self.rotation.r = rotation

    def setPosition(self, position):
        self.position = position
    
    def moveWheels(self, ratio1, ratio2):
        ratio1 = max(min(ratio1, 1), -1)
        ratio2 = max(min(ratio2, 1), -1)
        self.rightWheel.setVelocity(ratio1 * self.maxSpeed)
        self.leftWheel.setVelocity(ratio2 * self.maxSpeed)
    

    def getDiffToAng(self, ang):
        return self.rotation - ang
    
    def getDistToAng(self, ang):
        return Angle(d=max(round(self.rotation.d), ang.d) - min(self.rotation.d, ang.d))
    
    def rotateInPlace(self, direction, speedFract):
        self.moveWheels(direction[0] * speedFract, direction[1] * speedFract)
    
    def rotateSmoothly(self, direction, speedFract, ratio):
        if direction == [-1, 1]:
            self.moveWheels(ratio * speedFract, speedFract)
        else:
            self.moveWheels(speedFract, ratio * speedFract)
    
    def moveToCoords(self, coords):
        posDiff = substractLists(self.position, coords)
        ang = getAngFromCoords(posDiff)
        posDist = getDistance(posDiff)
        rotDist = self.getDistToAng(ang)
        rotDiff = self.getDiffToAng(ang)
        print("rotDiff:", rotDiff.d)
        print("traget ang: ", ang.d)
        
        if 180 > rotDiff.d > 0 or rotDiff.d < -180:
            direction = [1, -1]
        else:
            direction = [-1, 1]

        rotSpeed = mapVals(rotDist.d, 15, 2, 0.6, 1)
        if rotDist.d < 30:
            self.rotateSmoothly(direction, 1, rotSpeed)
            print("menos de 15")
        else:
            self.rotateInPlace(direction, 1)

        if posDist < 0.05:
            self.moveWheels(0, 0)
            return True


