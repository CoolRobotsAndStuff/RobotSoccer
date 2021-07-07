from RobotModell import RobotModell
from RobotController import Controller
from BallModell import Ball
import time

class MainController:
    def __init__(self, timeStep):
        # Important variables
        self.timeStep = timeStep
        
        # Controller
        self.controller = Controller(self.timeStep)

        # Objects
        self.robot1 = RobotModell(self.timeStep, "B1")
        self.robot2 = RobotModell(self.timeStep, "B2")
        self.robot3 = RobotModell(self.timeStep, "B3")
        self.ball = Ball()

        # World state variables
        self.waitingForKickoff = False

    
    def run(self):
        self.update()
        #self.robot1.moveWheels(0.5, -0.5)
        self.robot1.moveToCoords(self.ball.position)
        #self.robot1.rotateInPlace()

        print("Rotation:", self.robot1.rotationInDegs)
        print("Position:", self.robot1.position)

        

    def doLoop(self):
        return self.controller.doLoop()

    # Sincronizes the real world with the virtual representation of it
    def syncVirtualAndReal(self):
        worldData = self.controller.getWorldData()

        # Updating robots and controller
        for robot in (self.robot1, self.robot2, self.robot3):
            if robot.name == self.controller.name:
                self.controller.setVelocities(robot.rightWheel.getVelocity(), robot.leftWheel.getVelocity())
                self.controller.setPositions(robot.rightWheel.getPosition(), robot.leftWheel.getPosition())
            
            if worldData is not None:
                robotData = worldData[robot.name]
                robot.setPosition((robotData["x"], robotData["y"]))
                robot.setRotation(robotData["orientation"])
            
        
        # Updating ball
        self.ball.update()
        if worldData is not None:
            ballData = worldData["ball"]
            self.ball.setPosition((ballData["x"], ballData["y"]))

            # Updating world state variables
            self.waitingForKickoff = worldData["waiting_for_kickoff"]

    def update(self):
        self.syncVirtualAndReal()