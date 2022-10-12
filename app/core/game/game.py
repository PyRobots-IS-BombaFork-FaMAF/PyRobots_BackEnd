from robot import *

class game():

    def __init__(self, quantityRound):
        self.round = 1
        self.quantityRound = quantityRound
        self.listRobot = []
        self.listMove = []
        self.robotPosition = dict() 

    def add(self, robotList):
        self.listRobot.append(robotList)

    def AdvanceRound(self):
        if(self.round <= self.quantityRound):
            for robot in self.listRobot:
                robot.respond()
                #robot.__mover_robot()
                self.robotPosition = {
                                        'coords': robot.get_position(),
                                        'direction': robot.get_direction(),
                                        'speed': robot.get_velocity()
                                    }
                self.listMove.append(self.robotPosition)
            self.round += 1
            print(self.listMove)