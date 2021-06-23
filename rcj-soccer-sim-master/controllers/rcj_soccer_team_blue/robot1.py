# rcj_soccer_player controller - ROBOT B1

# Feel free to import built-in libraries
import math

# You can also import scripts that you put into the folder with controller
from rcj_soccer_robot import RCJSoccerRobot, TIME_STEP
from utilityFunctions import *


class MyRobot1(RCJSoccerRobot):

    def __init__(self, robot):
        super().__init__(robot)

        # Flags
        self.rotateToDegsFirstTime = True

    def run(self):
        r = False
        while self.robot.step(TIME_STEP) != -1:
            if self.is_new_data():
                data = self.get_new_data()

                # Get the position of our robot
                robotPos = data[self.name]
                # Get the position of the ball
                ballPos = data['ball']

                self.position = [robotPos["x"], robotPos["y"]]
                self.rotation = normalizeDegs(radsToDegs(robotPos["orientation"]) + 180)
                print(self.rotation)
                print(self.position)

                if not r:
                    r = self.moveToCoords([-0.3, -0.3])

                if r:
                    self.moveWheels(0, 0)

                # Moves the wheels at the specified ratio
    def moveWheels(self, leftRatio, rightRatio):
        self.leftWheel.move(leftRatio)
        self.rightWheel.move(rightRatio)

    def rotateToDegs(self, degs, orientation="closest", maxSpeed=0.7):
        accuracy = 2
        if self.rotateToDegsFirstTime:
            #print("STARTED ROTATION")
            self.seqRotateToDegsInitialRot = self.rotation
            self.seqRotateToDegsinitialDiff = round(self.seqRotateToDegsInitialRot - degs)
            self.rotateToDegsFirstTime = False
        diff = self.rotation - degs
        moveDiff = max(round(self.rotation), degs) - min(self.rotation, degs)
        if diff > 180 or diff < -180:
            moveDiff = 360 - moveDiff
        speedFract = min(mapVals(moveDiff, accuracy, 90, 0.2, 1), maxSpeed)
        if accuracy  * -1 < diff < accuracy or 360 - accuracy < diff < 360 + accuracy:
            self.rotateToDegsFirstTime = True
            return True
        else:
            if orientation == "closest":
                if 180 > self.seqRotateToDegsinitialDiff > 0 or self.seqRotateToDegsinitialDiff < -180:
                    direction = "right"
                else:
                    direction = "left"
            elif orientation == "farthest":
                if 180 > self.seqRotateToDegsinitialDiff > 0 or self.seqRotateToDegsinitialDiff < -180:
                    direction = "left"
                else:
                    direction = "right"
            else:
                direction = orientation
            if direction == "right":
                self.moveWheels(speedFract * -1, speedFract)
            elif direction == "left":
                self.moveWheels(speedFract, speedFract * -1)
            #print("speed fract: " +  str(speedFract))
            #print("target angle: " +  str(degs))
            #print("moveDiff: " + str(moveDiff))
            #print("diff: " + str(diff))
            #print("orientation: " + str(orientation))
            #print("direction: " + str(direction))
            #print("initialDiff: " + str(self.rotateToDegsinitialDiff))
        return False

    def moveToCoords(self, targetPos):
        errorMargin = 0.002
        descelerationStart = 0.5 * 0.12
        diffX = targetPos[0] - self.position[0]
        diffY = targetPos[1] - self.position[1]
        print("diff in pos: " + str(diffX) + " , " + str(diffY))
        dist = getDistance((diffX, diffY))
        #print("Dist: "+ str(dist))
        if errorMargin * -1 < dist < errorMargin:
            #self.robot.move(0,0)
            print("FinisehedMove")
            return True
        else:
            
            ang = getDegsFromCoords((diffX, diffY))
            ang = normalizeDegs(ang)
            print("traget ang: " + str(ang))
            ratio = min(mapVals(dist, 0, descelerationStart, 0.1, 1), 1)
            ratio = max(ratio, 0.8)
            if self.rotateToDegs(ang):
                self.moveWheels(ratio, ratio)
                print("Moving")
        return False
