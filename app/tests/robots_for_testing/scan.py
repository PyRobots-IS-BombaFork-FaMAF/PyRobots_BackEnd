from app.core.game.robot import Robot

class scan(Robot):
    count: int

    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            pass
        elif self.count == 1:
            self.point_scanner(45, 10)
        elif self.count == 2:
            self.scanned()
        self.count += 1