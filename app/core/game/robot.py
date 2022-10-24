from abc import abstractmethod
import math
from typing import Tuple



class Robot(object):
    """
    Class from which the users robots will inherit
    """
    _actual_velocity: float        # Velocity at witch the robot is actually moving
    _actual_direction: float       # Direction in witch the robot is actually moving
    _desired_velocity: float       # Velocity that was set by the robot
    _desired_direction: float      # Direction that was set by the robot
    _position: Tuple[float, float]
    _damage: float

    def __init__(self):
        self._actual_velocity = 0
        self._actual_direction = 0
        self._desired_velocity = 0
        self._desired_direction = 0
        self._position = (0,0)
        self._damage = 0

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    def move_robot(self):
        if self._actual_velocity < 50:
            self._actual_direction = self._desired_direction

        if abs(self._actual_velocity - self._desired_velocity) < 30:
            self._actual_velocity = self._desired_velocity
        elif (self._actual_velocity - self._desired_velocity) < 0:
            self._actual_velocity += 30
        else:
            self._actual_velocity += -30

        x = self._actual_velocity * math.cos(math.radians(self._actual_direction)) / 100
        y = self._actual_velocity * math.sin(math.radians(self._actual_direction)) / 100
        self._position = (self._position[0] + x, self._position[1] + y)

    #Status
    def get_direction(self):
        return self._actual_direction

    def get_velocity(self):
        return self._actual_velocity

    def get_position(self):
        return self._position

    def get_damage(self):
        return self._damage

    #Motor
    def drive(self, direction, velocity):
        if velocity < 100:
            self._desired_velocity = velocity
        else:
            self._desired_velocity = 100
        self._desired_direction = direction
