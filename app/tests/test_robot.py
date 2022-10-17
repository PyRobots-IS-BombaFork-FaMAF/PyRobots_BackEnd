from app.core.game.robot import *



def test_get_direction():
    r = Robot()
    r.direction = 20
    assert 20 == r.get_direction()

def test_get_velocity():
    r = Robot()
    r.velocity = 13
    assert 13 == r.get_velocity()

def test_get_damage():
    r = Robot()
    r.damage = 80
    assert 80 == r.get_damage()


def test_get_position():
    r = Robot()
    r.position = (213, 425)
    assert (213, 425) == r.get_position()

def test_drive():
    r = Robot()
    r.drive(45, 30)
    assert (45 == r.direction) and (r.velocity == 30)

def test_drive_speedlimit():
    r = Robot()
    r.drive(220, 99999999)
    assert r.velocity == 100
