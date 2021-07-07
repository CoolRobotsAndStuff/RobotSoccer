from UtilityFunctions import *
import struct

class Comunicator:

    def __init__(self, comunicator, timeStep):
        self.timeStep = timeStep
        self.device = comunicator
        self.device.enable(self.timeStep)
        self.robotNames = ("B1", "B2", "B3", "Y1", "Y2", "Y3")

    def parse_supervisor_msg(self, packet: str) -> dict:
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

    def get_new_data(self) -> dict:
        """Read new data from supervisor

        Returns:
            dict: See `parse_supervisor_msg` method
        """
        packet = self.device.getData()
        self.device.nextPacket()

        return self.parse_supervisor_msg(packet)

    def is_new_data(self) -> bool:
        """Check if there are new data to be received

        Returns:
            bool: Whether there is new data received from supervisor.
        """
        return self.device.getQueueLength() > 0