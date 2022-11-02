from app.core.game.robot import Robot

class scan2(Robot):
    count: int

    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            self.point_scanner(45, 10)
        elif self.count == 1:
            self.point_scanner(45, 0.0001)
        elif self.count == 2:
            self.point_scanner(0, 8)
        elif self.count == 3:
            self.point_scanner(0, 8)
        elif self.count == 4:
            self.point_scanner(5, 10)
        elif self.count == 5:
            self.point_scanner(5, 10)
        self.count += 1