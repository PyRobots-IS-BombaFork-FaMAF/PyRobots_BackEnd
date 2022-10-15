from robot import *
import json

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
                                        'name': robot.name,
                                        'rounds': [{
                                            'position': robot.get_position(),
                                            'direction': robot.get_direction(),
                                            'speed': robot.get_velocity()
                                        }],
                                        'cause_of_death?': "robot execution error"
                                    }
                jsonRobotPosition = json.dumps(self.robotPosition)
                self.listMove.append(jsonRobotPosition)
            self.round += 1 
        return self.listMove


r1 = Robot('robot_1')
r2 = Robot('robot_2')
r3 = Robot('robot_3')

juego = game(4)

juego.add(r1)
juego.add(r2)
juego.add(r3)



