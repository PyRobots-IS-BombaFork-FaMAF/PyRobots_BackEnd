import random
from typing import Any, Optional, Tuple, Union
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
    damage: float
    missile: Optional[tuple[float, float]]
    scanner_direction: Optional[float]
    resolution_in_degrees: Optional[float]

    def __init__(self, coords: tuple[float, float], direction: float, speed: float, damage: float,
                 scanner_direction: Optional[float] = None, resolution_in_degrees: Optional[float] = None,
                 missile: Optional[tuple[float, float]] = None):

        self.coords = coords
        self.direction = direction
        self.speed = speed
        self.damage = damage
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
            "speed": self.speed,
            "damage": self.damage
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
    is_cannon_ready: int # the rounds needed to that the canon is ready, if is <= 0 then the cannon is ready
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

        if for_animation:
            self.round_result_for_animation = RobotResult_round(self.position, self.direction, self.actual_velocity, self.damage)
            self.result_for_animation = RobotResult(
                name,
                [RobotResult_round(self.position, self.direction, self.actual_velocity, self.damage)],
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
        if self.is_alive():
            try:
                self.robot.respond()
            except:
                self.damage = 1
                self.cause_of_death = "robot execution error"


    def cannon_calculation(self, direction: float, distance: float) -> Tuple[float, float, int]:
        """
            Return the position and rounds to impact of the missile
        """

        direction = direction % 360
        distance = distance if distance < cannon_range else cannon_range

        x: float = distance * math.cos(math.radians(direction)) + self.position[0]
        y: float = distance * math.sin(math.radians(direction)) + self.position[1]

        x_explosion: float = board_size if x > board_size else (0 if x < 0 else x)
        y_explosion: float = board_size if y > board_size else (0 if y < 0 else y)

        rounds_to_explosion: int = distance // missile_velocity

        return (x_explosion, y_explosion, rounds_to_explosion)


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
        if x < 0 or x > board_size or y < 0 or y > board_size:
            self.apply_damage(0.02)

        # Check to prevent it from going out of bounds
        if (x < 0 or x > board_size) and (y < 0 or y > board_size):
            self.actual_velocity = 0
            self.desired_velocity = 0
        elif x < 0 or x > board_size:
            self.direction = 90 if y_component_direction >= 0 else 270
            self.actual_velocity = abs(y_component_direction * self.actual_velocity)
            self.desired_velocity = abs(y_component_direction * self.desired_velocity)
        elif y < 0 or y > board_size:
            self.direction = 0 if x_component_direction >= 0 else 180
            self.actual_velocity = abs(x_component_direction * self.actual_velocity)
            self.desired_velocity = abs(x_component_direction * self.desired_velocity)

        x = board_size if x > board_size else (0 if x < 0 else x)
        y = board_size if y > board_size else (0 if y < 0 else y)

        # Update position
        self.position = (x, y)

        # Update velocity
        self.actual_velocity += velocity_difference

        if self.result_for_animation != None:
            self.result_for_animation.rounds.append(
                RobotResult_round(
                    self.position, self.direction, self.actual_velocity, self.damage,
                    self.round_result_for_animation.scanner_direction,
                    self.round_result_for_animation.resolution_in_degrees,
                    self.round_result_for_animation.missile
                )
            )

    def is_alive(self) -> bool:
        return self.damage < 1

    def apply_damage(self, d: float):
        self.damage += d
        if self.damage >= 1:
            self.cause_of_death = "out of life"
            self.damage = 1

    def get_result_for_animation(self) -> Optional[RobotResult]:
        if self.result_for_animation != None:
            self.result_for_animation.cause_of_death = self.cause_of_death
        return self.result_for_animation




class GameState():
    round: int
    future_explosions: list[Tuple[float, float, int]]
    ourRobots: list[RobotInGame]

    for_animation: bool

    def __init__(self, robotClasses: list[Tuple[str, type]], for_animation: bool = False):
        """
            `robotClasses` is a dictionary of robot names and their classes
        """
        self.round = 0
        self.future_explosions = []
        self.ourRobots = [RobotInGame(robot[1], robot[0], for_animation) for robot in robotClasses]
        self.for_animation = for_animation

    def apply_explosion(self, x: int, y: int):
        for robotInGame in self.ourRobots:
            if robotInGame.is_alive():
                distance = math.sqrt((robotInGame.position[0] - x)**2 + (robotInGame.position[1] - y)**2)
                new_damage = 0    if distance > 40 else (
                             0.03 if distance > 20 else (
                             0.05 if distance > 5 else (
                             0.1 )))
                robotInGame.apply_damage(new_damage)

    def amount_of_robots_alive(self) -> int:
        return sum([1 for robot in self.ourRobots if robot.is_alive()])

    def advance_round(self):
        self.round += 1
        for robotInGame in self.ourRobots:
            if robotInGame.is_alive():
                robotInGame.executeRobotCode()

        # For scanner
        for robot in self.ourRobots:
            if robot.is_alive():
                direction: Any = robot.robot._scan_direction
                resolution: Any = robot.robot._resolution_in_degrees
                x1_position: float = robot.position[0]
                y1_position: float = robot.position[1]
                shortest_distance = float('inf')

                if (isinstance(direction, numbers.Real) and isinstance(resolution, numbers.Real)
                    and resolution <= 10 and resolution >= 0):
                    direction = direction % 360
                    for robotInGame in self.ourRobots:
                        if robotInGame is not robot and robotInGame.is_alive():
                            # Distance formula
                            x2_position: float = robotInGame.position[0]
                            y2_position: float = robotInGame.position[1]
                            distance: float = math.sqrt((x2_position-x1_position)**2+(y2_position-y1_position)**2)

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

        # Apply explosions
        new_future_explosion: list[Tuple[float, float, int]] = []
        for explosion in self.future_explosions:
            if explosion[2] == 0:
                self.apply_explosion(explosion[0], explosion[1])
            else:
                new_future_explosion.append((explosion[0], explosion[1], explosion[2] - 1))
        self.future_explosions = new_future_explosion.copy()

        # Apply collisions between robots
        for orRobot1 in self.ourRobots:
            for orRobot2 in self.ourRobots:
                if (orRobot1 is not orRobot2 and
                        orRobot1.is_alive() and orRobot2.is_alive() and
                        abs(orRobot1.position[0] - orRobot2.position[0]) < 1 and
                        abs(orRobot1.position[1] - orRobot2.position[1]) < 1):
                    orRobot1.apply_damage(0.1)
                    orRobot2.apply_damage(0.1)
                    # 0.1 of damage, because another 0.1 will be applied with `orRobot1`
                    # as `orRobot2` and vice versa

        # Shoot
        for robotInGame in self.ourRobots:
            if robotInGame.is_alive():
                shot_direction: Any = robotInGame.robot._shot_direction
                shot_distance: Any = robotInGame.robot._shot_distance
                if (robotInGame.is_cannon_ready <= 0 and
                        isinstance(shot_direction, numbers.Real) and
                        isinstance(shot_distance, numbers.Real) and shot_distance > 0):

                    shot_direction = shot_direction % 360
                    shot_distance = shot_distance if shot_distance < cannon_range else cannon_range

                    (x, y, rounds_to_impact) = robotInGame.cannon_calculation(shot_direction, shot_distance)
                    robotInGame.is_cannon_ready = rounds_to_reload
                    self.future_explosions.append((x, y, rounds_to_impact - 1)) # - 1 because these one counts
                    if self.for_animation:
                        robotInGame.round_result_for_animation.set_missile((shot_direction, shot_distance))
                elif self.for_animation:
                    robotInGame.round_result_for_animation.set_missile(None)
                robotInGame.is_cannon_ready -= 1


        # Move
        for robotInGame in self.ourRobots:
            if robotInGame.is_alive():
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
            if robotInGame.is_alive():
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
