from app.core.game.robot import Robot

class simple(Robot):
    count: int

    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            self.drive(45, 0.2)
        elif self.count == 1:
            pass
        elif self.count == 2:
            self.drive(135, 0.2)
        elif self.count == 3:
            self.drive(45, 0.4)
        elif self.count == 4:
            self.drive(60, 0.6)
        
        self.count += 1
