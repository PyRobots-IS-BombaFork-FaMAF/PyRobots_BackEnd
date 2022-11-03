from app.core.game.robot import Robot
from typing import Optional, Tuple
import random
import math

class attack1(Robot):
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
        self.robot_found = False

    def respond(self):
        try:
            direction = (self.last_scan_direction + 90) % 359 if not self.robot_found else self.last_scan_direction
            self.last_scan_direction = direction
            resolution = 5 if not self.robot_found else 1
            self.point_scanner(self.last_scan_direction, resolution)
            self.drive(direction, 50)
            self.robot_found = False
            if self.scanned() != float('inf') and self.round > 0:
                self.robot_found = True
                self.robot_localiced_distance = self.scanned()
                robot_localiced_x = self.robot_localiced_distance * math.cos(math.radians(self.last_scan_direction))
                robot_localiced_y = self.robot_localiced_distance * math.sin(math.radians(self.last_scan_direction))
                self.robot_localiced = (self.get_position()[0] + robot_localiced_x, self.get_position()[1] + robot_localiced_y)
                x = robot_localiced_x - self.get_position()[0]
                y = robot_localiced_y - self.get_position()[1]
                angle = math.atan2(y, x) * (180.0 / math.pi)
                anglediff = (direction - angle + 180 + 360) % 360 - 180
                self.drive(self.robot_localiced[0], 100)
                self.cannon(angle, 1000)
                self.point_scanner(anglediff, resolution)
            self.round += 1
        except Exception as e:
            print(f"Error {e.with_traceback(None)}")


