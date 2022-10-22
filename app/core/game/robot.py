from abc import abstractmethod



class Robot(object):
    """
    Clase from which the users robots will inherit
    """



    def __init__(self):
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

    def __mover_robot():
        pass


#Status
    def get_direction():
        return self.direction

    def get_velocity():
        return self.velocity

    def get_position():
        return self.position

    def get_damage():
        return self.damage


"""
metodos que hacen falta implementar:

  Cañon
    is_cannon_ready():
    cannon(degree, distance):

  Escaneo
    point_scanner(direction, resolution_in_degrees):
    scanned():

  Motor
    drive(direction, velocity):


"""
