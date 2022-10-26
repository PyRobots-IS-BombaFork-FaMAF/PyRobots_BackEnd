from app.core.game.robot import Robot

class invalid_drives(Robot):
    def initialize(self):
        self.count = 0

    def respond(self):
        if self.count == 0:
            self._set_direction = 1000
            self._set_velocity = 100
        elif self.count == 1:
            self._set_direction = -67.654
            self._set_velocity = -34.345
        elif self.count == 2:
            self._set_direction = "str"
            self._set_velocity = None
        elif self.count == 3:
            self._set_direction = [[0,1,2,3], ("dfjsl", "fdskjñ"), {8: 3, 7: "jk"}]
            self._set_velocity = lambda x: x/0

        self.count += 1