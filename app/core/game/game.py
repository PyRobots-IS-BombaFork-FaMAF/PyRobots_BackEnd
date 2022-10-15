from app.core.game.robot import *

class game():

    def __init__(self, quantityRound):
        self.round = 1
        if(quantityRound < 10000):
            self.quantityRound = quantityRound
        else:
            self.quantityRound = 10000
        self.listRobot = []
        self.listMove = []
        self.robotPosition = dict() 

    def add(self, robotList):
        self.listRobot.append(robotList)

    def advance_round(self):
        if(self.round <= self.quantityRound):
            for robot in self.listRobot:
                robot.respond()
                #robot.__mover_robot()
                cause_of_death = False
                self.robotPosition = {
                                        'name': robot.name,
                                        'rounds': [{
                                            'position': robot.get_position(),
                                            'direction': robot.get_direction(),
                                            'speed': robot.get_velocity()
                                        }]
                                    }
                if(cause_of_death):
                    self.robotPosition['cause_of_death?'] = "robot execution error"
                self.listMove.append(self.robotPosition)
            self.round += 1 
    
    def execute_simulacion(self):
        while(self.round <= self.quantityRound):
            self.advance_round()
        


