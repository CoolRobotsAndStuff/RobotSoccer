from UtilityFunctions import *
from angles import Angle

class Ball:

    def __init__(self):
        self.rotation = Angle(r=0)
        self.position = [0, 0]
        self.prevPosition = [0, 0]
        self.radious = 0
        self.time = 0
    
    def getRotationFromPos(self):
        if self.prevPosition != self.position:
            posDiff = [(self.position[0] - self.prevPosition[0]), (self.position[1] - self.prevPosition[1])]
            accuracy = getDistance(posDiff)
            #print("accuracy: " + str(accuracy))
            if accuracy > 0.001:
                return getAngFromCoords(posDiff)
        return None

    def setPosition(self, position):
        self.position = position

    def update(self):
        # Updates position
        self.prevPosition = self.position

        # Updates rotation
        rot = self.getRotationFromPos()
        if rot is not None:
            self.rotation = rot