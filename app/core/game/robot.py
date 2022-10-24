from abc import abstractmethod
from typing import Tuple, Optional



class Robot(object):
    """
    Class from which the users robots will inherit
    """
    _actual_velocity: float              # Velocity at witch the robot is actually moving
    _actual_direction: float             # Direction in witch the robot is actually moving
    _set_velocity: Optional[float]       # Velocity that was set by the robot
    _set_direction: Optional[float]      # Direction that was set by the robot
    _position: Tuple[float, float]
    _damage: float

    def __init__(self):
        self._actual_velocity = 0
        self._actual_direction = 0
        self._set_velocity = 0
        self._set_direction = 0
        self._position = (0,0)
        self._damage = 0

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def respond(self):
        pass

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
            self._set_velocity = velocity
        else:
            self._set_velocity = 100
        self._set_direction = direction
