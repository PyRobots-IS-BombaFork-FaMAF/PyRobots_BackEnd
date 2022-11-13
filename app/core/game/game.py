import random
from typing import Any, Dict, Optional, Tuple, Union
from app.core.game.robot import Robot
from types import ModuleType
from typing import NamedTuple
import math
from app.core.game.constants import *
import numbers



class RobotResult_round():
    coords: tuple[float, float]
    direction: float
    speed: float
    missile: Optional[tuple[float, float]]
    scanner_direction: Optional[float]
    resolution_in_degrees: Optional[float]

    def __init__(self, coords: tuple[float, float], direction: float, speed: float,
                 scanner_direction: Optional[float] = None, resolution_in_degrees: Optional[float] = None,
                 missile: Optional[tuple[float, float]] = None):

        self.coords = coords
        self.direction = direction
        self.speed = speed
        self.missile = missile
        self.scanner_direction = scanner_direction
        self.resolution_in_degrees = resolution_in_degrees

    def set_missile(self, missile: Optional[tuple[float, float]] = None):
        self.missile = missile

    def set_scanner(self, direction: Optional[float], resolution: Optional[float]):
        self.scanner_direction = direction
        self.resolution_in_degrees = resolution

    def json_output(self) -> dict:
        res = {
            "coords": {"x": self.coords[0], "y": self.coords[1]},
            "direction": self.direction,
            "speed": self.speed
        }
        if self.resolution_in_degrees != None and self.scanner_direction != None:
            res["scanner"] = {
                "direction": self.scanner_direction,
                "resolution_in_degrees": self.resolution_in_degrees
                }
        if self.missile != None:
            res["missile"] = { "direction": self.missile[0], "distance": self.missile[1] }
        return res

class RobotResult():
    name: str
    rounds: list[RobotResult_round]
    cause_of_death: Optional[str]

    def __init__(self, name: str, rounds: list[RobotResult_round], cause_of_death: Optional[str]):
        self.name = name
        self.rounds = rounds
        self.cause_of_death = cause_of_death

    def json_output(self) -> dict:
        res = {
            "name": self.name,
            "rounds": [round.json_output() for round in self.rounds]
        }
        if self.cause_of_death != None:
            res["cause_of_death"] = self.cause_of_death
        return res


class SimulationResult():
    """
    The result of the simulation for being converted to a JSON for the animation
    """

    robots: list[RobotResult]

    def __init__(self, robots: list[RobotResult]):
        self.robots = robots

    def json_output(self) -> dict:
        return {
            "board_size": board_size,
            "missile_velocity": missile_velocity,
            "robots": [robot.json_output() for robot in self.robots]
        }



class RobotInGame():
    name: str  # Only for generating the `json`
    robot: Robot
    position: tuple[float, float]
    actual_velocity: float   # m/round # Velocity at witch the robot is actually moving
    desired_velocity: float  # m/round # Velocity that was set by the robot
    direction: float  # degrees (so it is modulo 360)
    damage: float     # with damage ∈ [0;1) robot is alive
    cause_of_death: Optional[str]
    is_shooting: bool
    is_cannon_ready: int # the rounds needed to that the canon is ready, if is <= 0 then the cannon is ready
    explosions_points: list[tuple[float,float,int]] # list of missile impacts positions launched [x,y, rounds to impact]
    scanner_result: float

    round_result_for_animation: Optional[RobotResult_round]
    result_for_animation: Optional[RobotResult] # Only when animation is needed

    def __init__(self, robotClass: type, name: str, for_animation: bool):
        self.name = name
        self.cause_of_death = None
        self.position = (random.random() * board_size, random.random() * board_size)
        self.actual_velocity = 0
        self.desired_velocity = 0
        self.direction = 0
        self.damage = 0
        self.is_cannon_ready = 0
        self.is_shooting: False
        self.explosions_points = []

        if for_animation:
            self.round_result_for_animation = RobotResult_round(self.position, self.direction, self.actual_velocity)
            self.result_for_animation = RobotResult(
                name,
                [RobotResult_round(self.position, self.direction, self.actual_velocity)],
                None
            )
        else:
            self.result_for_animation = None
            self.round_result_for_animation = None

        try:
            # There are no robots that do not inherit from Robot because that is checked in upload
            self.robot = robotClass()

            # Update position of `robot`
            self.robot._position = self.position

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


    def explosion_calculation (self):
        self.is_cannon_ready += -1
        if (self.robot._is_shooting and self.is_cannon_ready <= 0 and
            isinstance(self.robot._shot_direction, numbers.Number) and
            isinstance(self.robot._shot_distance, numbers.Number)):

            direction = self.robot._shot_direction % 360
            distance = self.robot._shot_distance if self.robot._shot_distance < cannon_range else cannon_range

            x: float = distance * math.cos(math.radians(direction)) + self.position[0]
            y: float = distance * math.sin(math.radians(direction)) + self.position[1]

            x_explosion: float = board_size if x > board_size else (0 if x < 0 else x)
            y_explosion: float = board_size if y > board_size else (0 if y < 0 else y)

            rounds_to_explosion: int = distance // missile_velocity

            explosion = (x_explosion, y_explosion, rounds_to_explosion)
            self.explosions_points.append(explosion)

            self.is_shooting = False
            self.is_cannon_ready = rounds_to_reload

            # If animation is needed add the missile shot to re result of the round
            if self.result_for_animation != None:
                self.round_result_for_animation.set_missile((direction, distance))
        elif self.result_for_animation != None:
            self.round_result_for_animation.set_missile()


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

        self.desired_velocity = velocity

        # Update direction
        if direction != None and self.actual_velocity <= max_velocity/2:
            self.direction = direction % 360

        x_component_direction: float = math.cos(math.radians(self.direction))
        y_component_direction: float = math.sin(math.radians(self.direction))

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
        unused_acceleration: float = 1 - used_acceleration
        x_movement: float = (
            x_velocity
            + x_component_direction * acceleration * used_acceleration**2 / 2
                * math.copysign(1, velocity_difference)
            + x_component_direction * unused_acceleration * velocity_difference
        )
        y_movement: float = (
            y_velocity
            + y_component_direction * acceleration * used_acceleration**2 / 2
                * math.copysign(1, velocity_difference)
            + y_component_direction * unused_acceleration * velocity_difference
        )

        # Calculate new position
        x: float = self.position[0] + x_movement
        y: float = self.position[1] + y_movement

        # Check to prevent it from going out of bounds
        x = board_size if x > board_size else (0 if x < 0 else x)
        y = board_size if y > board_size else (0 if y < 0 else y)

        # Update position
        self.position = (x, y)

        # Update velocity
        self.actual_velocity += velocity_difference

        if self.result_for_animation != None:
            self.result_for_animation.rounds.append(
                RobotResult_round(
                    self.position, self.direction, self.actual_velocity,
                    self.round_result_for_animation.scanner_direction,
                    self.round_result_for_animation.resolution_in_degrees,
                    self.round_result_for_animation.missile
                )
            )

    def get_result_for_animation(self) -> Optional[RobotResult]:
        if self.result_for_animation != None:
            self.result_for_animation.cause_of_death = self.cause_of_death
        return self.result_for_animation




class GameState():
    round: int
    ourRobots: list[RobotInGame]

    for_animation: bool

    def __init__(self, robotClasses: list[Tuple[str, type]], for_animation: bool = False):
        """
            `robotClasses` is a dictionary of robot names and their classes
        """
        self.round = 0
        self.ourRobots = [RobotInGame(robot[1], robot[0], for_animation) for robot in robotClasses]
        self.for_animation = for_animation

    def amount_of_robots_alive(self) -> int:
        return sum([1 for robot in self.ourRobots if robot.damage < 1])

    def advance_round(self):
        self.round += 1
        for robotInGame in self.ourRobots:
            # Execute `robotInGame.robot` code if it is alive
            if robotInGame.damage < 1:
                robotInGame.executeRobotCode()

        # For scanner
        for robot in self.ourRobots:
            if robot.damage < 1:
                direction: Any = robot.robot._scan_direction
                resolution: Any = robot.robot._resolution_in_degrees
                x1_position: float = robot.position[0]
                y1_position: float = robot.position[1]
                shortest_distance = float('inf')

                if (isinstance(direction, numbers.Real) and isinstance(resolution, numbers.Real)
                    and resolution <= 10 and resolution >= 0):
                    direction = direction % 360
                    for robotInGame in self.ourRobots:
                        if robotInGame is not robot and robotInGame.damage < 1:
                            # Distance formula
                            x2_position: float = robotInGame.position[0]
                            y2_position: float = robotInGame.position[1]
                            distance = math.sqrt((x2_position-x1_position)**2+(y2_position-y1_position)**2)

                            # Angle formula
                            x = x2_position - x1_position
                            y = y2_position - y1_position
                            angle = math.atan2(y, x) * (180.0 / math.pi)
                            angleDiff = (direction - angle + 180 + 360) % 360 - 180
                            if angleDiff >= -resolution and angleDiff <= resolution and distance < shortest_distance:
                                shortest_distance = distance
                    robot.scanner_result = shortest_distance
                    if robot.round_result_for_animation != None:
                        robot.round_result_for_animation.set_scanner(direction, resolution)
                else:
                    robot.scanner_result = None

        # Shoot
        for robotInGame in self.ourRobots:
            if robotInGame.damage < 1:
                # Calculate the position and de round where the missile shots will explote
                robotInGame.explosion_calculation()


        # Move
        for robotInGame in self.ourRobots:
            if robotInGame.damage < 1:
                # Extract new velocity and direction from `robotInGame.robot`
                set_velocity: Any = robotInGame.robot._set_velocity
                set_direction: Any = robotInGame.robot._set_direction
                # They are of type `Any` because the robot code may have set anything

                # Check types
                if not isinstance(set_velocity, numbers.Real):
                    set_velocity = None
                if not isinstance(set_direction, numbers.Real):
                    set_direction = None

                # Update movement of `RobotInGame`
                robotInGame.updateOurRobot_movement(set_velocity, set_direction)


        # Update `Robot` fields
        for robotInGame in self.ourRobots:
            if robotInGame.damage < 1:
                robotInGame.robot._set_velocity = None
                robotInGame.robot._set_direction = None
                robotInGame.robot._position = robotInGame.position
                robotInGame.robot._actual_velocity = robotInGame.actual_velocity
                robotInGame.robot._actual_direction = robotInGame.direction
                robotInGame.robot._damage = robotInGame.damage
                robotInGame.robot._is_shooting = False
                robotInGame.robot._is_cannon_ready = robotInGame.is_cannon_ready <= 0
                robotInGame.robot._last_scanned = robotInGame.scanner_result
                robotInGame.robot._scan_direction = None
                robotInGame.robot._resolution_in_degrees = None
                robotInGame.robot._shot_direction = None
                robotInGame.robot._shot_distance = None

    def get_result_for_animation(self) -> Optional[SimulationResult]:
        if self.for_animation:
            return SimulationResult([robot.get_result_for_animation() for robot in self.ourRobots])
        else:
            return None


class RobotInput(NamedTuple):
    pathToCode: str # In python format (e.g. 'app.robot_code.robot1')
    robotClassName: str
    name: str # For JSON output


def getRobots(robots: list[RobotInput]) -> list[type]:
    """
    Get the robots classes from the given paths
    Paths are in python format (e.g. `'app.robot_code.robot1'`)
    """
    def getRobot(pathToRobot: str, robotClassName: str) -> type:
        robotModule: ModuleType = __import__(pathToRobot, fromlist=[robotClassName])
        robotClass: type = getattr(robotModule, robotClassName)
        return robotClass

    return list(map(lambda robotInput: getRobot(robotInput.pathToCode, robotInput.robotClassName), robots))


def runSimulation(robots: list[RobotInput], rounds: int, for_animation: bool = False) -> Union[SimulationResult, list[int]]:
    """
    Run a simulation with the robots on the given paths.
    Paths are in python format (e.g. `'app.robot_code.robot1'`).

    If `for_animation` is `True` the result will be a `SimulationResult` object.
    Otherwise will be, the index of surviving robots. So if it is a list of one element, the element
    will be the index of the winner. If it has no element it is because all robots died. And if it has
    more than one element, it is because there was a tie.
    """

    robotsClasses: list[type] = getRobots(robots)
    robotsNames: list[str] = list(map((lambda robot: robot.name), robots))

    gameState: GameState = GameState(list(zip(robotsNames, robotsClasses)), for_animation)

    while gameState.amount_of_robots_alive() > 1 and gameState.round < rounds:
        gameState.advance_round()

    if for_animation:
        return gameState.get_result_for_animation()
    else:
        return [robotsNames.index(robot.name) for robot in gameState.ourRobots if robot.damage < 1]
