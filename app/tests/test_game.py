from turtle import speed
from app.core.game.game import *
from app.core.game.robot import *



def test_empty_RobotInGame():
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

    # Result should have 2 round
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

    # Result should have 3 rounds
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

    position2 = robot.position # for later

    # Make a more complex movement
    robot.updateOurRobot_movement(velocity=0.3, direction=135)

    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0     # When collisions are implemented, this may change
    assert robot.direction == 135
    assert robot.actual_velocity == 0.3
    assert robot.desired_velocity == 0.3
    assert abs(robot.position[0] - (position2[0] - math.cos(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors
    assert abs(robot.position[1] - (position2[1] + math.sin(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors

    # Result should have 4 rounds
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 4
    assert robot.result_for_animation.rounds[0].coords == position
    assert robot.result_for_animation.rounds[0].direction == 0
    assert robot.result_for_animation.rounds[0].speed == 0
    assert robot.result_for_animation.rounds[1].coords == position
    assert robot.result_for_animation.rounds[1].direction == 0
    assert robot.result_for_animation.rounds[1].speed == 0
    assert robot.result_for_animation.rounds[2].coords == position2
    assert robot.result_for_animation.rounds[2].direction == 0
    assert robot.result_for_animation.rounds[2].speed == 0.1
    assert robot.result_for_animation.rounds[3].coords == robot.position
    assert robot.result_for_animation.rounds[3].direction == 135
    assert robot.result_for_animation.rounds[3].speed == 0.3


    # Test result for animation
    result_for_animation = robot.get_result_for_animation()
    assert result_for_animation.name == 'empty'
    assert result_for_animation.cause_of_death == None
    assert len(result_for_animation.rounds) == 4
    assert result_for_animation.rounds[0].coords == position
    assert result_for_animation.rounds[0].direction == 0
    assert result_for_animation.rounds[0].speed == 0
    assert result_for_animation.rounds[1].coords == position
    assert result_for_animation.rounds[1].direction == 0
    assert result_for_animation.rounds[1].speed == 0
    assert result_for_animation.rounds[2].coords == position2
    assert result_for_animation.rounds[2].direction == 0
    assert result_for_animation.rounds[2].speed == 0.1
    assert result_for_animation.rounds[3].coords == robot.position
    assert result_for_animation.rounds[3].direction == 135
    assert result_for_animation.rounds[3].speed == 0.3


def test2_RobotInGame():
    import app.tests.robots_for_testing.simple as simple

    robot: RobotInGame = RobotInGame(simple.simple, 'simple', False)

    assert robot.name == 'simple'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.direction == 0
    assert robot.actual_velocity == 0
    assert robot.desired_velocity == 0

    position = robot.position
    assert 0 <= position[0] and position[0] <= 1000
    assert 0 <= position[1] and position[1] <= 1000

    # NOTE: When we add collisions, the robot may day in the following tests

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position2 = robot.position
    assert abs(position2[0] - (position[0] + 0.1 * math.cos(math.pi/4))) < 0.00001
    assert abs(position2[1] - (position[1] + 0.1 * math.sin(math.pi/4))) < 0.00001

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position3 = robot.position
    assert abs(position3[0] - (position2[0] + 0.2 * math.cos(math.pi/4))) < 0.00001
    assert abs(position3[1] - (position2[1] + 0.2 * math.sin(math.pi/4))) < 0.00001

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position4 = robot.position
    assert abs(position4[0] - (position3[0] - 0.2 * math.cos(math.pi/4))) < 0.00001
    assert abs(position4[1] - (position3[1] + 0.2 * math.sin(math.pi/4))) < 0.00001

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position5 = robot.position
    assert abs(position5[0] - (position4[0] + 0.3 * math.cos(math.pi/4))) < 0.00001
    assert abs(position5[1] - (position4[1] + 0.3 * math.sin(math.pi/4))) < 0.00001

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position6 = robot.position
    assert abs(position6[0] - (position5[0] + 0.5 * math.cos(math.pi/3))) < 0.00001
    assert abs(position6[1] - (position5[1] + 0.5 * math.sin(math.pi/3))) < 0.00001

def testExceptions_RobotInGame():
    import app.tests.robots_for_testing.exception_init as exception_init

    robot: RobotInGame = RobotInGame(exception_init.exception_init, 'exception_init', False)

    assert robot.name == 'exception_init'
    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1

def testExceptions2_RobotInGame():
    import app.tests.robots_for_testing.exception_initialize as exception_initialize

    robot: RobotInGame = RobotInGame(exception_initialize.exception_initialize, 'exception_initialize', False)

    assert robot.name == 'exception_initialize'
    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1

def testExceptions3_RobotInGame():
    import app.tests.robots_for_testing.exception_respond as exception_respond

    robot: RobotInGame = RobotInGame(exception_respond.exception_respond, 'exception_respond', False)

    assert robot.name == 'exception_respond'

    assert robot.cause_of_death == None
    assert robot.damage == 0

    robot.executeRobotCode()

    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1

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