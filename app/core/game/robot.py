from abc import abstractmethod
import math
#import numpy as np



class Robot(object):
    """
    Class from which the users robots will inherit
    """

    def __init__(self):
        self.actual_velocity = 0
        self.actual_direction = 0
        self.velocity = 0
        self.direction = 0
        self.position = (0,0)
        self.damage = 0

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def respond(self):
        pass

    def move_robot(self):
        if self.actual_velocity < 50:
            self.actual_direction = self.direction

        if abs(self.actual_velocity - self.velocity) < 30:
            self.actual_velocity = self.velocity
        elif (self.actual_velocity - self.velocity) < 0:
            self.actual_velocity += 30
        else:
            self.actual_velocity += -30

        x = self.actual_velocity * math.cos(math.radians(self.direction)) / 100
        y = self.actual_velocity * math.sin(math.radians(self.direction)) / 100
        self.position = (self.position[0] + x, self.position[1] + y)

#Status
    def get_direction(self):
        return self.direction

    def get_velocity(self):
        return self.velocity

    def get_position(self):
        return self.position

    def get_damage(self):
        return self.damage

#Motor
    def drive(self, direction, velocity):
        if velocity < 100:
            self.velocity = velocity
        else:
            self.velocity = 100
        self.direction = direction

"""
metodos que hacen falta implementar:

  Cañon
    is_cannon_ready():
    cannon(degree, distance):

  Escaneo
    point_scanner(direction, resolution_in_degrees):
    scanned():
"""
