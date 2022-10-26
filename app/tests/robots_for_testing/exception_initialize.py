from app.core.game.robot import Robot

class exception_initialize(Robot):
    def initialize(self):
        raise Exception('exception_initialize')

    def respond(self):
        pass
