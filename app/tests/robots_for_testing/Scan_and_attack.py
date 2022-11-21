# Robot que escnea en todas las direcciones, y cuendo encuentra otro robot
# ataca y avanza en esa dirección hasta que lo pierde de vista
from app.core.game.robot import Robot
from typing import Optional
import random

class Scan_and_attack(Robot):
    round: int
    state: Optional[str]

    searching_last_direction: Optional[float]
    last_scan: Optional[float]

    def initialize(self):
        self.round = 0
        self.state = None
        self.searching_last_direction = None
        self.last_scan = None

    def respond(self):
        try:
            if self.state == None:
                self.state = "searching"
                self.searching_last_direction = random.uniform(0, 360)
                self.point_scanner(self.searching_last_direction, 10)
            elif self.state == "searching":
                self.last_scan = self.scanned()
                if self.last_scan == float('inf'):
                    self.searching_last_direction += 10
                    self.point_scanner(self.searching_last_direction, 10)
                elif self.last_scan > 100:
                    self.state = "moving and attacking"
                    self.drive(self.searching_last_direction, 50)
                    self.cannon(self.searching_last_direction, self.last_scan)
                    self.point_scanner(self.searching_last_direction, 10)
                else:
                    self.state = "attacking"
                    self.drive(self.searching_last_direction, 0)
                    self.point_scanner(self.searching_last_direction, 10)
            elif self.state == "moving and attacking":
                self.last_scan = self.scanned()
                if self.last_scan == float('inf'):
                    self.state = "searching"
                    self.searching_last_direction += 10
                    self.point_scanner(self.searching_last_direction, 10)
                elif self.last_scan > 100:
                    self.drive(self.searching_last_direction, 50)
                    self.cannon(self.searching_last_direction, self.last_scan)
                    self.point_scanner(self.searching_last_direction, 10)
                else:
                    self.state = "attacking"
                    self.drive(self.searching_last_direction, 0)
                    self.point_scanner(self.searching_last_direction, 10)
            elif self.state == "attacking":
                self.cannon(self.searching_last_direction, self.last_scan)
                self.last_scan = self.scanned()
                if self.last_scan == float('inf'):
                    self.state = "searching"
                    self.searching_last_direction += 10
                self.point_scanner(self.searching_last_direction, 10)

            self.round += 1
        except Exception as e:
            print(e)
