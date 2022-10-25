import random
from typing import Any, Optional
from app.core.game.robot import Robot
from types import ModuleType
from typing import NamedTuple
import math



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





max_velocity: float = 1   # m/round
acceleration: float = 0.2    # m/round²  # also limit of deceleration
board_size: int = 1000     # m

class RobotInGame():
    name: str  # Only for generating the `json`
    robot: Robot
    position: tuple[float, float]
    actual_velocity: float   # m/round # Velocity at witch the robot is actually moving
    desired_velocity: float  # m/round # Velocity that was set by the robot
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
            # There are no robots that do not inherit from Robot because that is checked in upload
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

    def updateOurRobot_movement(self,
                velocity: Optional[float] = None, direction: Optional[float] = None
            ):
        # Validate velocity
        if velocity == None:
            velocity = self.desired_velocity
        if velocity < 0:
            velocity = 0
        if velocity > max_velocity:
            velocity = max_velocity

        # Update direction
        if direction != None and self.actual_velocity <= max_velocity/2:
            self.direction = direction % 360
        
        x_component_direction: float = abs(math.cos(math.radians(self.direction)))
        y_component_direction: float = abs(math.sin(math.radians(self.direction)))

        # Calculate velocity difference
        velocity_difference: float = (
                min(acceleration, velocity - self.actual_velocity)
            if self.actual_velocity <= velocity else # for == the to formulas give the same
                max(-acceleration, velocity - self.actual_velocity)
        )

        x_velocity: float = self.actual_velocity * x_component_direction
        y_velocity: float = self.actual_velocity * y_component_direction

        # We have to take into account that the robot may be accelerating or decelerating in part or all of the round
        used_acceleration: float = abs(velocity_difference / acceleration)
        x_movement: float = x_velocity + x_component_direction * used_acceleration / 2
        y_movement: float = y_velocity + y_component_direction * used_acceleration / 2

        # Update position
        self.position[0] += x_movement
        self.position[1] += y_movement

        # Update velocity
        self.actual_velocity += velocity_difference


class GameState():
    round: int
    ourRobots: list[RobotInGame]

    def __init__(self, robotClasses: list[type]):
        self.round = 0
        self.ourRobots = list(map((lambda robotClass: RobotInGame(robotClass)), robotClasses))

    def advance_round(self):
        self.round += 1
        for robotInGame in self.ourRobots:
            # Execute `robotInGame.robot` code if it is alive
            if robotInGame.damage < 1:
                robotInGame.executeRobotCode()

        for robotInGame in self.ourRobots:
            if robotInGame.damage < 1:
                # Extract new velocity and direction from `robotInGame.robot`
                set_velocity: Any = robotInGame.robot._set_velocity
                set_direction: Any = robotInGame.robot._set_direction
                # They are of type `Any` because the robot code may have set anything

                # Check types
                if not isinstance(set_velocity, float):
                    set_velocity = None
                if not isinstance(set_direction, float):
                    set_direction = None

                # Update movement of `RobotInGame`
                robotInGame.updateOurRobot_movement(set_velocity, set_direction)

        # NOTE: When adding scanning and cannon, more `for`s will be needed

        # Update `Robot` fields
        for robotInGame in self.ourRobots:
            if robotInGame.damage < 1:
                robotInGame.robot._set_velocity = None
                robotInGame.robot._set_direction = None
                robotInGame.robot._position = robotInGame.position
                robotInGame.robot._actual_velocity = robotInGame.actual_velocity
                robotInGame.robot._actual_direction = robotInGame.direction
                robotInGame.robot._damage = robotInGame.damage
        
        # TODO: Make something for the results for the animation


def getRobots(pathsToRobots: list[str]) -> list[type]:
    """
    Get the robots classes from the given paths
    Paths are in python format (e.g. `'app.robot_code.robot1'`)
    """
    def getRobot(pathToRobot: str) -> type:
        robatClassName: str = pathToRobot.split('.')[-1]
        robotModule: ModuleType = __import__(pathToRobot, fromlist=[robatClassName])
        robotClass: type = getattr(robotModule, robatClassName)
        return robotClass
    
    return list(map(getRobot, pathsToRobots))


class RobotInput(NamedTuple):
    pathToCode: str # In python format (e.g. 'app.robot_code.robot1')
    name: str # For JSON output

def runSimulation(robots: list[RobotInput], rounds: int) -> SimulationResult:
    """
    Run a simulation with the robots on the given paths
    Paths are in python format (e.g. `'app.robot_code.robot1'`)
    """

    robotsFiles: list[str] = list(map((lambda robot: robot.pathToCode), robots))

    robotsClasses: list[type] = getRobots(robotsFiles)

    # TODO: Create a `GameState`
    # TODO: Advance all rounds

    pass




