from app.core.game.robot import *



def test_get_direction():
    r = Robot()
    r._actual_direction = 20
    assert 20 == r.get_direction()

def test_get_velocity():
    r = Robot()
    r._actual_velocity = 13
    assert 13 == r.get_velocity()

def test_get_damage():
    r = Robot()
    r._damage = 80
    assert 80 == r.get_damage()


def test_get_position():
    r = Robot()
    r._position = (213, 425)
    assert (213, 425) == r.get_position()

def test_drive():
    r = Robot()
    r.drive(45, 30)
    assert (45 == r._desired_direction) and (r._desired_velocity == 30)

def test_drive_speedlimit():
    r = Robot()
    r.drive(220, 99999999)
    assert r._desired_velocity == 100


def test_meve_robot():
    r = Robot()
    r._actual_velocity = 100
    r._actual_direction = 90
    r.drive(45,100)
    r.move_robot()

    assert (round(r._position[0]), r._position[1]) == (0,1)
