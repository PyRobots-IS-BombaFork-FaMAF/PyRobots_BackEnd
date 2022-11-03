from app.core.game.robot import *



def test_get_direction():
    r = Robot()
    r._actual_direction = 20
    assert 20 == r.get_direction()

def test_get_velocity():
    r = Robot()
    r._actual_velocity = 0.13
    assert 13 == r.get_velocity()

def test_get_damage():
    r = Robot()
    r._damage = 0.8
    assert 80 == r.get_damage()


def test_get_position():
    r = Robot()
    r._position = (213, 425)
    assert (213, 425) == r.get_position()

def test_drive():
    r = Robot()
    r.drive(45, 30)
    assert (45 == r._set_direction) and (r._set_velocity == 0.3)

def test_drive_speedlimit():
    r = Robot()
    r.drive(220, 99)
    assert r._set_velocity == 0.99
    assert r._set_direction == 220


def test_is_cannon_ready():
    r = Robot()
    assert r._is_cannon_ready == True

def test_cannon():
    r = Robot()
    r.cannon(300, 450)
    assert r._shot[0] == 300
    assert r._shot[1] == 450
    assert r._is_shooting == True
