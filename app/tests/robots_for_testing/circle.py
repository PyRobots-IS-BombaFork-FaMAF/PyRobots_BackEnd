from app.core.game.robot import Robot

class circle(Robot):
    round: int
    angle: int

    def initialize(self):
        self.round = 0
        self.angle = 0

    def respond(self):
        self.drive(self.angle, 50)
        self.angle += 1
        self.round += 1