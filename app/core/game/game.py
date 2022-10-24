import random
import app.core.models.robot_models as robot_models
from typing import Optional
from app.core.game.robot import Robot
from types import ModuleType
from typing import NamedTuple


class RobotResult_round(NamedTuple):
    coords: tuple[float, float]
    direction: float
    speed: float

class RobotResult(NamedTuple):
            
    name: str
    rounds: list[RobotResult_round]
    cause_of_death: Optional[str]

class SimulationResult(NamedTuple):
    """
    The result of the simulation for being converted to a JSON for the animation
    """

    robots: list[RobotResult]





max_velocity: float = 10   # m/round
acceleration: float = 2    # m/round²
deceleration: float = -2   # m/round²
board_size: int = 1000     # m

class RobotInGame():
    name: str  # Only for generating the `json`
    robot: Robot
    position: tuple[float, float]
    velocity: float   # m/round
    direction: float  # degrees (so it is modulo 360)
    damage: float     # with damage ∈ [0;1) robot is alive
    cause_of_death: Optional[str]

    def __init__(self, robotClass: type, name: str):
        self.name = name
        self.cause_of_death = None
        self.position = (random.random() * board_size, random.random() * board_size)
        self.velocity = 0
        self.direction = 0
        self.damage = 0
        try:
            self.robot = robotClass()
            self.robot.initialize()
        except:
            self.damage = 1
            self.cause_of_death = "robot execution error"

    def executeRobotCode(self):
        if self.damage < 1:
            try:
                self.robot.respond()
            except:
                self.damage = 1
                self.cause_of_death = "robot execution error"

    def updateOurRobot_movement(self, velocity: float, direction: float):
        if velocity < 0:
            velocity = 0
        if velocity > max_velocity:
            velocity = max_velocity

        direction = direction % 360

        # TODO: Update velocity


        # TODO: Update direction


class GameState():
    round: int
    ourRobots: list[RobotInGame]

    def __init__(self, robotClasses: list[type]):
        self.round = 0
        self.ourRobots = list(map((lambda robotClass: RobotInGame(robotClass)), robotClasses))

    def advance_round(self):
        self.round += 1
        for robotInGame in self.ourRobots:

            # If robot is alive:
                # TODO: Execute `robotInGame.robot` code if it is alive
                # TODO: Extract new velocity and direction from `robotInGame.robot`
                # TODO: Update `RobotInGame` with `updateOurRobot_movement`
                # TODO: Update `robotInGame.robot` fields

            # NOTE: When adding scanning and cannon, multiple `for`s will be needed
            pass


def getRobots(pathsToRobots: list[str]) -> list[type]:
    """
    Get the robots classes from the given paths
    """
    robotsModules: list[ModuleType] = list(map((lambda path: __import__(path, fromlist='.'.join(path.split('.')[1:]))), pathsToRobots))
    robotsNames: list[str] = list(map((lambda path: path.split('.')[-1]), pathsToRobots))

    robotsClasses: list[type] = []
    for i in range(len(robotsModules)):
        robotsClasses.append(getattr(robotsModules[i], robotsNames[i]))

    return robotsClasses


def runSimulation(robots: list[robot_models.Robot], rounds: int) -> SimulationResult:
    """
    Run a simulation with the robots on the given paths
    """

    robotsFiles: list[str] = list(map((lambda robot: robot.code), robots))

    robotsClasses: list[type] = getRobots(robotsFiles)

    # TODO: Create a `GameState`
    # TODO: Advance all rounds

    pass




