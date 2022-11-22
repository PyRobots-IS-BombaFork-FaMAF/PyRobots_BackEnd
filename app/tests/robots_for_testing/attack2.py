from app.core.game.robot import Robot
from typing import Optional, Tuple
import math

class attack2(Robot):
    round: int
    angle: int

    last_scan_direction: Optional[float]
    robot_localiced: Optional[Tuple[float, float]]
    robot_localiced_distance: Optional[float]

    def initialize(self):
        self.round = 0
        self.angle = 0
        self.robot_localiced = None
        self.robot_localiced_distance = None
        self.last_scan_direction = 0

    def respond(self):
        try:
            direction = (self.last_scan_direction + 90) % 360 
            self.last_scan_direction = direction
            self.point_scanner(self.last_scan_direction, 10)
            self.drive(self.get_position()[0], 50)
            if self.scanned() != float('inf') and self.round > 0:
                self.robot_localiced_distance = self.scanned()
                robot_localiced_x = self.robot_localiced_distance * math.cos(math.radians(self.last_scan_direction))
                robot_localiced_y = self.robot_localiced_distance * math.sin(math.radians(self.last_scan_direction))
                self.robot_localiced = (self.get_position()[0] + robot_localiced_x, self.get_position()[1] + robot_localiced_y)
                self.drive(self.robot_localiced[0], 50)
            
            if self.robot_localiced_distance != None:
                self.cannon(self.last_scan_direction, 1000)
            self.round += 1
        except Exception as e:
            print(f"Error {e.with_traceback(None)}")


