from controller import Robot
import math
from utilityFunctions import *
import struct

class Comunicator:

    def __init__(self, comunicator, timeStep):
        self.timeStep = timeStep
        self.device = comunicator
        self.device.enable(self.timeStep)
        self.robotNames = ("B1", "B2", "B3", "Y1", "Y2", "Y3")

    def parseSupervisorMsg(self, packet: str) -> dict:
        """Parse message received from supervisor

        Returns:
            dict: Location info about each robot and the ball.
            Example:
                {
                    'B1': {'x': 0.0, 'y': 0.2, 'orientation': 1},
                    'B2': {'x': 0.4, 'y': -0.2, 'orientation': 1},
                    ...
                    'ball': {'x': -0.7, 'y': 0.3},
                    'waiting_for_kickoff': False,
                }
        """
        # X, Z and rotation for each robot
        # plus X and Z for ball
        # plus True/False telling whether the goal was scored
        nOfRobots = len(self.robotNames)

        struct_fmt = 'ddd' * nOfRobots + 'dd' + '?'

        unpacked = struct.unpack(struct_fmt, packet)

        data = {}
        for i, r in enumerate(self.robotNames):
            data[r] = {
                "x": unpacked[3 * i],
                "y": unpacked[3 * i + 1],
                "orientation": unpacked[3 * i + 2]
            }
        ball_data_index = 3 * nOfRobots
        data["ball"] = {
            "x": unpacked[ball_data_index],
            "y": unpacked[ball_data_index + 1]
        }

        waiting_for_kickoff_data_index = ball_data_index + 2
        data["waiting_for_kickoff"] = unpacked[waiting_for_kickoff_data_index]
        return data

    def getNewData(self) -> dict:
        """Read new data from supervisor

        Returns:
            dict: See `parse_supervisor_msg` method
        """
        packet = self.device.getData()
        self.device.nextPacket()

        return self.parseSupervisorMsg(packet)

    def isNewData(self) -> bool:
        """Check if there are new data to be received

        Returns:
            bool: Whether there is new data received from supervisor.
        """
        return self.device.getQueueLength() > 0

# Controlls a wheel
class Wheel:
    def __init__(self, device):
        self.wheel = device
        self.wheel.setPosition(float("inf"))
        self.wheel.setVelocity(0)
    
    def setPosition(self, position):
        self.wheel.setPosition(position)
    
    def setVelocity(self, velocity):
        self.wheel.setVelocity(velocity)

# Abstraction layer for robot
class ControllerLayer:
    def __init__(self, timeStep):
        # Important variables

        self.timeStep = timeStep
        self.robot = Robot()

        # Identification
        self.name = self.robot.getName()
        self.team = self.name[0]
        self.playerId = int(self.name[1])
        
        # Components
        self.leftWheel = Wheel(self.robot.getDevice("left wheel motor"))
        self.rightWheel = Wheel(self.robot.getDevice("right wheel motor"))
        self.comunicator = Comunicator(self.robot.getDevice("receiver"), self.timeStep)
    
    def doLoop(self):
        return self.robot.step(self.timeStep) != -1
    
    def setVelocities(self, rightVelocity, leftVelocity):
        self.rightWheel.setVelocity(rightVelocity)
        self.leftWheel.setVelocity(leftVelocity)
    
    def setPositions(self, rightPosition, leftPosition):
        self.rightWheel.setPosition(rightPosition)
        self.leftWheel.setPosition(leftPosition)
    
    def getWorldData(self):
        wd = None
        while self.comunicator.isNewData():
            wd = self.comunicator.getNewData()
        if wd is not None:
            print(self.name, wd["ball"]["x"], self.robot.getTime())
        return wd