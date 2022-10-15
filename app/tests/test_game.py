from app.core.game.game import *
from app.core.game.robot import *

r1 = Robot('robot_1')

juego = game(4)

juego.add(r1)

def test_add_list():

    round = len(juego.listMove)
    juego.advance_round()
    round1 = len(juego.listMove)

    assert round + 1 == round1

def test_same_quantity_round():
    juego.execute_simulacion()

    assert len(juego.listMove) == juego.quantityRound

def test_quantity_round():
    game1 = game(100012314)

    assert game1.quantityRound == 10000

def test_add_robot():
    robotListLen = len(juego.listRobot)
    r2 = Robot('robot_2')
    juego.add(r2)
    robotListLen1 = len(juego.listRobot)

    assert robotListLen + 1 == robotListLen1