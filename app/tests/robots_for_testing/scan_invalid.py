from app.core.game.robot import Robot

class scan_invalid(Robot):
    count: int

    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            self.drive(45, 20)
            self.point_scanner(45, 20)
        elif self.count == 1:
            self.scanned()
        if self.count == 2:
            self.point_scanner(45, -1)
        elif self.count == 3:
            self.scanned()
        self.count += 1
