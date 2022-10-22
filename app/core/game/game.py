from app.core.game.robot import *
from types import ModuleType

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
                robot.move_robot()
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





def runSimulation(pathsToRobots: 'list[str]') -> 'list[dict[str, any]]':
    """
    Run a simulation with the robots on the given paths
    Paths are in python format (e.g. 'app.robot_code.robot1')
    """

    robotsModules: 'list[ModuleType]' = list(map((lambda path: __import__(path, fromlist='.'.join(path.split('.')[1:]))), pathsToRobots))
    robotsNames: 'list[str]' = list(map((lambda path: path.split('.')[-1]), pathsToRobots))

    robotsClasses: 'list[type]' = []
    for i in range(len(robotsModules)):
        robotsClasses.append(getattr(robotsModules[i], robotsNames[i]))

    robots: 'list[Robot]' = list(map(lambda robotClass: robotClass(), robotsClasses))


    pass





