from app.core.game.robot import Robot

class exception_respond(Robot):
    def initialize(self):
        pass

    def respond(self):
        raise Exception('exception_respond')
