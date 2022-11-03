from app.core.game.robot import Robot
from app.core.game.constants import *

class bad_aim_shooter(Robot):
    count: int

    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            pass
        elif self.count == 1:
            self.cannon(0, 1000)
        elif self.count == rounds_to_reload + 1:
            self.cannon(90, 1000)
        elif self.count == 2*rounds_to_reload + 1:
            self.cannon(180, 1000)
        elif self.count == 3*rounds_to_reload + 1:
            self.cannon(270, 1000)

        self.count += 1
