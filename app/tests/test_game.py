from turtle import speed
from app.core.game.game import *
from app.core.game.robot import *



def test_RobotInGame():
    import app.tests.robots_for_testing.empty as empty

    robot: RobotInGame = RobotInGame(empty.empty, 'empty', True)

    # `RobotInGame` fields
    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.direction == 0
    assert robot.actual_velocity == 0
    assert robot.desired_velocity == 0
    assert 0 <= robot.position[0] and robot.position[0] <= 1000
    assert 0 <= robot.position[1] and robot.position[1] <= 1000

    position = robot.position # for later

    # `RobotInGame.robot` fields
    assert robot.robot._actual_direction == 0
    assert robot.robot._actual_velocity == 0
    assert robot.robot._set_velocity == 0
    assert robot.robot._set_direction == 0
    assert robot.robot._position == robot.position
    assert robot.robot._damage == 0

    # `RobotInGame.result_for_animation` fields
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 1
    assert robot.result_for_animation.rounds[0].coords == robot.position
    assert robot.result_for_animation.rounds[0].direction == 0
    assert robot.result_for_animation.rounds[0].speed == 0

    # Execute robot code
    robot.executeRobotCode()
    robot.updateOurRobot_movement()

    # fields should not have changed because velocity is 0
    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.direction == 0
    assert robot.actual_velocity == 0
    assert robot.desired_velocity == 0
    assert robot.position == position

    # Result should have 1 round
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 2
    assert robot.result_for_animation.rounds[0].coords == position
    assert robot.result_for_animation.rounds[0].direction == 0
    assert robot.result_for_animation.rounds[0].speed == 0
    assert robot.result_for_animation.rounds[1].coords == position
    assert robot.result_for_animation.rounds[1].direction == 0
    assert robot.result_for_animation.rounds[1].speed == 0

    # Now wi will make the robot move
    robot.updateOurRobot_movement(velocity=0.1, direction=0)
    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0     # When collisions are implemented, this may change
    assert robot.direction == 0
    assert robot.actual_velocity == 0.1
    assert robot.desired_velocity == 0.1
    assert abs(robot.position[0] - (position[0] + 0.075)) < 0.00001 # There may be rounding errors
    assert robot.position[1] == position[1]

    # Result should have 2 rounds
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 3
    assert robot.result_for_animation.rounds[0].coords == position
    assert robot.result_for_animation.rounds[0].direction == 0
    assert robot.result_for_animation.rounds[0].speed == 0
    assert robot.result_for_animation.rounds[1].coords == position
    assert robot.result_for_animation.rounds[1].direction == 0
    assert robot.result_for_animation.rounds[1].speed == 0
    assert robot.result_for_animation.rounds[2].coords == robot.position
    assert robot.result_for_animation.rounds[2].direction == 0
    assert robot.result_for_animation.rounds[2].speed == 0.1




""" r1 = Robot('robot_1')

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

    assert robotListLen + 1 == robotListLen1 """