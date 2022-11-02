from app.core.game.robot import Robot

class shooter(Robot):
    count: int

    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            pass
        elif self.count == 1:
            self.cannon(0, 300)
        elif self.count == 3:
            self.cannon(90, 400)
        elif self.count == 5:
            self.cannon(0, 1000)
        self.count += 1
