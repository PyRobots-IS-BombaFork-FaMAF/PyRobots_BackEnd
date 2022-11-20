from app.core.game.robot import *

def test_empty_getters():
    r = Robot()
    assert r.get_damage() == 0
    assert r.get_velocity() == 0
    assert r.scanned() == None
    assert r.is_cannon_ready()

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
    assert 45 == r._set_direction
    assert r._set_velocity == 0.3

    r._actual_velocity = 0.3
    r._actual_direction = 45

    assert r.get_direction() == 45
    assert r.get_velocity() == 30

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
    assert r._shot_direction == 300
    assert r._shot_distance == 450
    assert r._is_shooting == True

    r._is_cannon_ready = True
    assert r.is_cannon_ready()
    r._is_cannon_ready = False
    assert not r.is_cannon_ready()


def test_scan():
    r = Robot()
    r.point_scanner(45, 10)
    assert r._scan_direction == 45
    assert r._resolution_in_degrees == 10

    r._last_scanned = 100
    assert r.scanned() == 100
