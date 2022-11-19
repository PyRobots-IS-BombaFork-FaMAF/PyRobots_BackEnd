from app.core.game.game import *
from app.core.game.robot import *
from app.core.game.constants import *

import math



def test_empty_RobotInGame():
    import app.tests.robots_for_testing.empty as empty

    robot: RobotInGame = RobotInGame(empty.empty, 'empty', True)

    # `RobotInGame` fields
    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()
    assert robot.direction == 0
    assert robot.actual_velocity == 0
    assert robot.desired_velocity == 0
    assert 0 <= robot.position[0] and robot.position[0] <= 1000
    assert 0 <= robot.position[1] and robot.position[1] <= 1000

    random_position = (robot.position[0], robot.position[1])

    robot.position = (400, 600)
    robot.robot._position = (400, 600)

    position = robot.position # for later

    # `RobotInGame.robot` fields
    assert robot.robot._actual_direction == 0
    assert robot.robot._actual_velocity == 0
    assert robot.robot._set_velocity == None
    assert robot.robot._set_direction == None
    assert robot.robot._position == robot.position
    assert robot.robot._damage == 0

    # `RobotInGame.result_for_animation` fields
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 1
    assert robot.result_for_animation.rounds[0].coords == random_position
    assert robot.result_for_animation.rounds[0].direction == 0
    assert robot.result_for_animation.rounds[0].speed == 0

    # Execute robot code
    robot.executeRobotCode()
    robot.updateOurRobot_movement()

    # fields should not have changed because velocity is 0
    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()
    assert robot.direction == 0
    assert robot.actual_velocity == 0
    assert robot.desired_velocity == 0
    assert robot.position == position

    # Result should have 2 round
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 2
    assert robot.result_for_animation.rounds[0].coords == random_position
    assert robot.result_for_animation.rounds[0].direction == 0
    assert robot.result_for_animation.rounds[0].speed == 0
    assert robot.result_for_animation.rounds[1].coords == position
    assert robot.result_for_animation.rounds[1].direction == 0
    assert robot.result_for_animation.rounds[1].speed == 0

    # Now wi will make the robot move
    robot.updateOurRobot_movement(velocity=0.1, direction=0)
    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()
    assert robot.direction == 0
    assert robot.actual_velocity == 0.1
    assert robot.desired_velocity == 0.1
    assert abs(robot.position[0] - (position[0] + 0.075)) < 0.00001 # There may be rounding errors
    assert robot.position[1] == position[1]

    # Result should have 3 rounds
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 3
    assert robot.result_for_animation.rounds[0].coords == random_position
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
    assert robot.damage == 0
    assert robot.is_alive()
    assert robot.direction == 135
    assert robot.actual_velocity == 0.3
    assert robot.desired_velocity == 0.3
    assert abs(robot.position[0] - (position2[0] - math.cos(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors
    assert abs(robot.position[1] - (position2[1] + math.sin(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors

    # Result should have 4 rounds
    assert robot.result_for_animation.name == 'empty'
    assert robot.result_for_animation.cause_of_death == None
    assert len(robot.result_for_animation.rounds) == 4
    assert robot.result_for_animation.rounds[0].coords == random_position
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
    result_for_animation: RobotResult = robot.get_result_for_animation()
    assert result_for_animation.name == 'empty'
    assert result_for_animation.cause_of_death == None
    assert len(result_for_animation.rounds) == 4
    assert result_for_animation.rounds[0].coords == random_position
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

    position3 = robot.position # for later

    robot.updateOurRobot_movement(velocity=0.1, direction=135)

    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()
    assert robot.direction == 135
    assert robot.actual_velocity == 0.1
    assert robot.desired_velocity == 0.1
    assert abs(robot.position[0] - (position3[0] - math.cos(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors
    assert abs(robot.position[1] - (position3[1] + math.sin(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors

    json_output = result_for_animation.json_output()

    assert json_output == {
        'name': 'empty',
        'rounds': [
            { 'coords': {'x': random_position[0], 'y': random_position[1] }, 'direction': 0, 'speed': 0, 'damage': 0 },
            { 'coords': {'x': position[0], 'y': position[1] }, 'direction': 0, 'speed': 0, 'damage': 0 },
            { 'coords': {'x': position2[0], 'y': position2[1] }, 'direction': 0, 'speed': 0.1, 'damage': 0 },
            { 'coords': {'x': position3[0], 'y': position3[1] }, 'direction': 135, 'speed': 0.3, 'damage': 0 },
            { 'coords': {'x': robot.position[0], 'y': robot.position[1] }, 'direction': 135, 'speed': 0.1, 'damage': 0 }
        ]
    }

def test2_RobotInGame():
    import app.tests.robots_for_testing.simple as simple

    robot: RobotInGame = RobotInGame(simple.simple, 'simple', False)

    assert robot.name == 'simple'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()
    assert robot.direction == 0
    assert robot.actual_velocity == 0
    assert robot.desired_velocity == 0

    assert 0 <= robot.position[0] and robot.position[0] <= 1000
    assert 0 <= robot.position[1] and robot.position[1] <= 1000
    robot.position = (347.543425423, 908.5412)
    robot.robot._position = (347.543425423, 908.5412)

    position = robot.position

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position2 = robot.position
    assert abs(position2[0] - (position[0] + 0.1 * math.cos(math.pi/4))) < 0.00001
    assert abs(position2[1] - (position[1] + 0.1 * math.sin(math.pi/4))) < 0.00001
    assert robot.is_alive()

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position3 = robot.position
    assert abs(position3[0] - (position2[0] + 0.2 * math.cos(math.pi/4))) < 0.00001
    assert abs(position3[1] - (position2[1] + 0.2 * math.sin(math.pi/4))) < 0.00001
    assert robot.is_alive()

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position4 = robot.position
    assert abs(position4[0] - (position3[0] - 0.2 * math.cos(math.pi/4))) < 0.00001
    assert abs(position4[1] - (position3[1] + 0.2 * math.sin(math.pi/4))) < 0.00001
    assert robot.is_alive()

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position5 = robot.position
    assert abs(position5[0] - (position4[0] + 0.3 * math.cos(math.pi/4))) < 0.00001
    assert abs(position5[1] - (position4[1] + 0.3 * math.sin(math.pi/4))) < 0.00001
    assert robot.is_alive()

    robot.executeRobotCode()
    robot.updateOurRobot_movement(robot.robot._set_velocity, robot.robot._set_direction)
    position6 = robot.position
    assert abs(position6[0] - (position5[0] + 0.5 * math.cos(math.pi/3))) < 0.00001
    assert abs(position6[1] - (position5[1] + 0.5 * math.sin(math.pi/3))) < 0.00001
    assert robot.is_alive()

    assert robot.get_result_for_animation() == None


def testExceptions_RobotInGame():
    import app.tests.robots_for_testing.exception_init as exception_init

    robot: RobotInGame = RobotInGame(exception_init.exception_init, 'exception_init', False)

    assert robot.name == 'exception_init'
    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1
    assert not robot.is_alive()

    assert robot.get_result_for_animation() == None

def testExceptions2_RobotInGame():
    import app.tests.robots_for_testing.exception_initialize as exception_initialize

    robot: RobotInGame = RobotInGame(exception_initialize.exception_initialize, 'exception_initialize', False)

    assert robot.name == 'exception_initialize'
    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1
    assert not robot.is_alive()

    assert robot.get_result_for_animation() == None

def testExceptions3_RobotInGame():
    import app.tests.robots_for_testing.exception_respond as exception_respond

    robot: RobotInGame = RobotInGame(exception_respond.exception_respond, 'exception_respond', False)

    assert robot.name == 'exception_respond'

    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()

    robot.executeRobotCode()

    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1
    assert not robot.is_alive()

    assert robot.get_result_for_animation() == None

def testInvalidDrives_RobotInGame():
    import app.tests.robots_for_testing.invalid_drives as invalid_drives

    robot: RobotInGame = RobotInGame(invalid_drives.invalid_drives, 'invalid_drives', False)

    assert robot.name == 'invalid_drives'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()

    robot.executeRobotCode()
    robot.executeRobotCode()
    robot.executeRobotCode()
    robot.executeRobotCode()

    assert robot.name == 'invalid_drives'
    assert robot.cause_of_death == None
    assert robot.damage == 0
    assert robot.is_alive()

    robot.updateOurRobot_movement(-3, 365)
    robot.updateOurRobot_movement(100, 365)
    assert robot.is_alive()

    assert robot.get_result_for_animation() == None

def testGameState():
    import app.tests.robots_for_testing.empty as empty
    import app.tests.robots_for_testing.simple as simple
    import app.tests.robots_for_testing.exception_init as exception_init
    import app.tests.robots_for_testing.exception_respond as exception_respond

    game: GameState = GameState(
        [
            ('empty', empty.empty),
            ('simple', simple.simple),
            ('exception_init', exception_init.exception_init),
            ('exception_respond', exception_respond.exception_respond)
        ],
        for_animation=True
    )

    assert game.round == 0
    assert len(game.ourRobots) == 4
    assert game.ourRobots[0].name == 'empty'
    assert game.ourRobots[1].name == 'simple'
    assert game.ourRobots[2].name == 'exception_init'
    assert game.ourRobots[3].name == 'exception_respond'

    assert game.ourRobots[0].cause_of_death == None
    assert game.ourRobots[1].cause_of_death == None
    assert game.ourRobots[2].cause_of_death == "robot execution error"
    assert game.ourRobots[3].cause_of_death == None

    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage == 0
    assert game.ourRobots[2].damage == 1
    assert game.ourRobots[3].damage == 0

    assert game.ourRobots[0].direction == 0
    assert game.ourRobots[1].direction == 0
    assert game.ourRobots[2].direction == 0
    assert game.ourRobots[3].direction == 0

    assert game.ourRobots[0].actual_velocity == 0
    assert game.ourRobots[1].actual_velocity == 0
    assert game.ourRobots[2].actual_velocity == 0
    assert game.ourRobots[3].actual_velocity == 0

    assert game.ourRobots[0].desired_velocity == 0
    assert game.ourRobots[1].desired_velocity == 0
    assert game.ourRobots[2].desired_velocity == 0
    assert game.ourRobots[3].desired_velocity == 0

    assert 0 <= game.ourRobots[0].position[0] <= 1000 and 0 <= game.ourRobots[0].position[1] <= 1000
    assert 0 <= game.ourRobots[1].position[0] <= 1000 and 0 <= game.ourRobots[1].position[1] <= 1000
    assert 0 <= game.ourRobots[2].position[0] <= 1000 and 0 <= game.ourRobots[2].position[1] <= 1000
    assert 0 <= game.ourRobots[3].position[0] <= 1000 and 0 <= game.ourRobots[3].position[1] <= 1000

    robot0_position0 = (game.ourRobots[0].position[0], game.ourRobots[0].position[1])
    robot1_position0 = (game.ourRobots[1].position[0], game.ourRobots[1].position[1])

    game.advance_round()

    assert game.round == 1

    assert game.ourRobots[0].cause_of_death == None
    assert game.ourRobots[1].cause_of_death == None
    assert game.ourRobots[2].cause_of_death == "robot execution error"
    assert game.ourRobots[3].cause_of_death == "robot execution error"

    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage <= 0.02 # May have collided with the wall
    assert game.ourRobots[2].damage == 1
    assert game.ourRobots[3].damage == 1

    assert game.ourRobots[0].position[0] == robot0_position0[0]
    assert game.ourRobots[0].position[1] == robot0_position0[1]
    assert abs(game.ourRobots[1].position[0] - (robot1_position0[0] + 0.1 * math.cos(math.pi/4))) < 0.00001
    assert abs(game.ourRobots[1].position[1] - (robot1_position0[1] + 0.1 * math.sin(math.pi/4))) < 0.00001

    game.advance_round()

    assert game.round == 2

    result_for_animation: SimulationResult = game.get_result_for_animation()

    assert len(result_for_animation.robots) == 4
    assert len(result_for_animation.robots[0].rounds) == 3
    assert len(result_for_animation.robots[1].rounds) == 3
    assert len(result_for_animation.robots[2].rounds) == 1
    assert len(result_for_animation.robots[3].rounds) == 1

    json_output = result_for_animation.json_output()

    assert 'board_size' in json_output.keys()
    assert 'missile_velocity' in json_output.keys()
    assert 'robots' in json_output.keys()
    assert len(json_output['robots']) == 4
    assert len(json_output['robots'][0]['rounds']) == 3
    assert len(json_output['robots'][1]['rounds']) == 3
    assert len(json_output['robots'][2]['rounds']) == 1
    assert len(json_output['robots'][3]['rounds']) == 1

def testGameState_noAnimation():
    import app.tests.robots_for_testing.empty as empty
    import app.tests.robots_for_testing.simple as simple

    game: GameState = GameState(
        [
            ('empty', empty.empty),
            ('simple', simple.simple)
        ],
        for_animation=False
    )

    assert game.round == 0

    game.advance_round()

    assert game.round == 1

    assert game.get_result_for_animation() == None


def testRunSimulation():
    robotsForSimulation: list[RobotInput] = [
        RobotInput('app.tests.robots_for_testing.empty', 'empty', 'Empty robot'),
        RobotInput('app.tests.robots_for_testing.exception_init', 'exception_init', 'Throws exception')
    ]

    simulationResult = runSimulation(robotsForSimulation, 5, False)

    assert simulationResult == [0]

def testRunSimulation2():
    robotsForSimulation: list[RobotInput] = [
        RobotInput('app.tests.robots_for_testing.empty', 'empty', 'Empty robot'),
        RobotInput('app.tests.robots_for_testing.simple', 'simple', 'Simple robot')
    ]

    simulationResult = runSimulation(robotsForSimulation, 5, False)

    assert simulationResult == [0, 1] # To little rounds for death be collisions

def testRunSimulation_forAnimation():
    robotsForSimulation: list[RobotInput] = [
        RobotInput('app.tests.robots_for_testing.empty', 'empty', 'Empty robot'),
        RobotInput('app.tests.robots_for_testing.simple', 'simple', 'Simple robot'),
        RobotInput('app.tests.robots_for_testing.exception_initialize', 'exception_initialize', 'Throws exception'),
        RobotInput('app.tests.robots_for_testing.invalid_drives', 'invalid_drives', 'Drives bad')
    ]

    simulationResult = runSimulation(robotsForSimulation, 5, True)

    assert isinstance(simulationResult, SimulationResult)

    assert len(simulationResult.robots) == 4
    assert len(simulationResult.robots[0].rounds) == 6
    assert len(simulationResult.robots[1].rounds) == 6
    assert len(simulationResult.robots[2].rounds) == 1
    assert len(simulationResult.robots[3].rounds) == 6

    assert simulationResult.robots[0].name == 'Empty robot'
    assert simulationResult.robots[1].name == 'Simple robot'
    assert simulationResult.robots[2].name == 'Throws exception'
    assert simulationResult.robots[3].name == 'Drives bad'

    assert simulationResult.robots[0].cause_of_death == None
    assert simulationResult.robots[1].cause_of_death == None # To little rounds for death be collisions
    assert simulationResult.robots[2].cause_of_death == "robot execution error"
    assert simulationResult.robots[3].cause_of_death == None


def test_damage():
    import app.tests.robots_for_testing.empty as empty

    robot: RobotInGame = RobotInGame(empty.empty, "empty", False)

    assert robot.is_alive()
    assert robot.damage == 0

    robot.apply_damage(0.1)
    assert robot.is_alive()
    assert robot.damage == 0.1

    robot.apply_damage(0.8)
    assert robot.is_alive()
    assert robot.damage == 0.9

    robot.apply_damage(0.2)
    assert not robot.is_alive()
    assert robot.damage == 1

    robot.apply_damage(200)
    assert not robot.is_alive()
    assert robot.damage == 1


def test_shoot():
    import app.tests.robots_for_testing.shooter as shooter
    game: GameState = GameState(
        [
            ('shooter', shooter.shooter)
        ],
        for_animation=True
    )

    game.ourRobots[0].position = (500, 500)

    game.advance_round()
    game.advance_round()

    assert game.future_explosions[0] == (800, 500, 84)

    for x in range(rounds_to_reload):
        game.advance_round()

    assert len(game.future_explosions) == 2
    assert game.future_explosions[0] == (800, 500, 24)
    assert game.future_explosions[1] == (500, 900, 113)

    game.ourRobots[0].position = (10, 10)

    for x in range(rounds_to_reload):
        game.advance_round()

    assert len(game.future_explosions) == 2
    assert game.future_explosions[0] == (500, 900, 53)
    assert game.future_explosions[1] == (710, 10, 199)


def test_shoot_out_of_bound():
    import app.tests.robots_for_testing.bad_aim_shooter as bad_aim_shooter
    game: GameState = GameState(
        [
            ('bad_aim_shooter', bad_aim_shooter.bad_aim_shooter)
        ],
        for_animation= False
    )

    game.ourRobots[0].position = (500, 500)

    game.advance_round()
    game.advance_round()

    assert game.future_explosions[0][0] == board_size
    assert abs(game.future_explosions[0][1] - 500) < 0.00001
    assert game.future_explosions[0][2] == 199

    for x in range(rounds_to_reload):
        game.advance_round()

    assert abs(game.future_explosions[1][0] - 500) < 0.00001
    assert game.future_explosions[1][1] == board_size
    assert game.future_explosions[1][2] == 199

    for x in range(rounds_to_reload):
        game.advance_round()

    assert game.future_explosions[2][0] == 0
    assert abs(game.future_explosions[2][1] - 500) < 0.00001
    assert game.future_explosions[2][2] == 199

    for x in range(rounds_to_reload):
        game.advance_round()

    assert abs(game.future_explosions[3][0] - 500) < 0.00001
    assert game.future_explosions[3][1] == 0
    assert game.future_explosions[3][2] == 199


def test_missiles_json():
    import app.tests.robots_for_testing.shooter as shooter
    game: GameState = GameState(
        [
            ('shooter', shooter.shooter)
        ],
        for_animation=True
    )

    game.advance_round()
    game.advance_round()

    for x in range(2*rounds_to_reload):
        game.advance_round()

    result_for_animation: SimulationResult = game.get_result_for_animation()
    json_output = result_for_animation.json_output()

    assert json_output['robots'][0]['rounds'][2]['missile'] != None
    assert json_output['robots'][0]['rounds'][2 + rounds_to_reload]['missile'] != None
    assert json_output['robots'][0]['rounds'][2 + 2*rounds_to_reload]['missile'] != None


def test_scanner_invalid():
    import app.tests.robots_for_testing.scan_invalid as scan_invalid
    game: GameState = GameState(
        [
            ('scan_invalid', scan_invalid.scan_invalid)
        ],
        for_animation=True
    )

    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[0].cause_of_death == None

    assert game.round == 0

    assert len(game.ourRobots) == 1

    game.advance_round()

    assert game.round == 1
    assert game.ourRobots[0].scanner_result == None
    assert game.ourRobots[0].robot._last_scanned == None

    game.advance_round()
    assert game.round == 2
    game.advance_round()
    assert game.round == 3
    assert game.ourRobots[0].scanner_result == None
    assert game.ourRobots[0].robot._last_scanned == None


def test_scanner():
    import app.tests.robots_for_testing.scan as scan
    import app.tests.robots_for_testing.empty as empty
    game: GameState = GameState(
        [
            ('scan', scan.scan),
            ('empty', empty.empty)
        ],
        for_animation=True
    )

    assert game.round == 0

    assert len(game.ourRobots) == 2
    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage == 0
    assert game.ourRobots[0].name == 'scan'
    assert game.ourRobots[1].name == 'empty'

    game.ourRobots[0].position = (0,0)

    game.ourRobots[1].position = (999,999)

    game.advance_round()

    assert game.round == 1

    game.advance_round()

    assert game.round == 2

    assert game.ourRobots[0].scanner_result != None
    assert game.ourRobots[0].robot._last_scanned != None
    assert game.ourRobots[0].robot._last_scanned == 1412.799348810722


def test_scanner2():
    import app.tests.robots_for_testing.scan2 as scan2
    import app.tests.robots_for_testing.empty as empty

    game: GameState = GameState(
        [
            ('scan', scan2.scan2),
            ('empty', empty.empty),
            ('empty', empty.empty),
            ('empty', empty.empty)
        ]
    )

    game.ourRobots[0].position = (500, 500)

    game.ourRobots[1].position = (600, 601)
    game.ourRobots[2].position = (499.99999, 499.99999)
    game.ourRobots[3].position = (510, 555)

    game.advance_round()

    assert game.ourRobots[0].scanner_result == math.sqrt(100**2 + 101**2)
    assert game.ourRobots[0].robot._last_scanned == math.sqrt(100**2 + 101**2)
    assert game.ourRobots[0].robot._scan_direction == None
    assert game.ourRobots[0].robot._resolution_in_degrees == None

    game.ourRobots[1].position = (620, 620)
    game.ourRobots[2].position = (600, 601)
    game.ourRobots[3].position = (800, 800)

    game.advance_round()

    assert game.ourRobots[0].scanner_result == math.sqrt(120**2 + 120**2)
    assert game.ourRobots[0].robot._last_scanned == math.sqrt(120**2 + 120**2)
    assert game.ourRobots[0].robot._scan_direction == None
    assert game.ourRobots[0].robot._resolution_in_degrees == None

    game.ourRobots[1].position = (700, 501)
    game.ourRobots[2].position = (800, 499)
    game.ourRobots[3].position = (499.99999, 500)

    game.advance_round()

    assert game.ourRobots[0].scanner_result == math.sqrt(1**2 + 200**2)
    assert game.ourRobots[0].robot._last_scanned == math.sqrt(1**2 + 200**2)
    assert game.ourRobots[0].robot._scan_direction == None
    assert game.ourRobots[0].robot._resolution_in_degrees == None

    game.ourRobots[1].position = (900, 501)
    game.ourRobots[2].position = (800, 499)
    game.ourRobots[3].position = (1000, 1000)

    game.advance_round()

    assert game.ourRobots[0].scanner_result == math.sqrt(1**2 + 300**2)
    assert game.ourRobots[0].robot._last_scanned == math.sqrt(1**2 + 300**2)
    assert game.ourRobots[0].robot._scan_direction == None
    assert game.ourRobots[0].robot._resolution_in_degrees == None

    game.ourRobots[1].position = (900, 501)
    game.ourRobots[2].position = (800, 499)
    game.ourRobots[3].position = (1000, 1000)

    game.advance_round()

    assert game.ourRobots[0].scanner_result == math.sqrt(1**2 + 300**2)
    assert game.ourRobots[0].robot._last_scanned == math.sqrt(1**2 + 300**2)
    assert game.ourRobots[0].robot._scan_direction == None
    assert game.ourRobots[0].robot._resolution_in_degrees == None

    game.ourRobots[1].position = (520, 660)
    game.ourRobots[2].position = (800, 499)
    game.ourRobots[3].position = (1000, 1000)

    game.advance_round()

    assert game.ourRobots[0].scanner_result == math.sqrt(300**2 + 1**2)
    assert game.ourRobots[0].robot._last_scanned == math.sqrt(300**2 + 1**2)
    assert game.ourRobots[0].robot._scan_direction == None
    assert game.ourRobots[0].robot._resolution_in_degrees == None


def test_drive_out_of_bounds():
    import app.tests.robots_for_testing.empty as empty
    game: GameState = GameState(
        [
            ('empty', empty.empty)
        ],
        for_animation=True
    )

    game.ourRobots[0].robot._set_velocity = 1
    game.ourRobots[0].actual_velocity = 1
    game.ourRobots[0].desired_velocity = 1

    game.ourRobots[0].direction = 0
    game.ourRobots[0].robot._set_direction = 0
    game.ourRobots[0].position = (board_size - 1, 10)

    assert game.ourRobots[0].damage == 0

    game.advance_round()
    assert game.ourRobots[0].position == (board_size, 10)
    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[0].actual_velocity == 1
    assert game.ourRobots[0].desired_velocity == 1
    assert game.ourRobots[0].direction == 0
    game.advance_round()
    assert game.ourRobots[0].position == (board_size, 10)
    assert game.ourRobots[0].damage == 0.02
    assert abs(game.ourRobots[0].actual_velocity) <= 0.00001
    assert abs(game.ourRobots[0].desired_velocity) <= 0.00001
    assert game.ourRobots[0].direction == 90


    game.ourRobots[0].robot._set_velocity = 1
    game.ourRobots[0].actual_velocity = 1
    game.ourRobots[0].desired_velocity = 1

    game.ourRobots[0].direction = 90
    game.ourRobots[0].robot._set_direction = 90
    game.ourRobots[0].position = (10, board_size - 1)

    game.advance_round()
    assert game.ourRobots[0].position == (10, board_size)
    assert game.ourRobots[0].damage == 0.02
    assert game.ourRobots[0].actual_velocity == 1
    assert game.ourRobots[0].desired_velocity == 1
    assert game.ourRobots[0].direction == 90
    game.advance_round()
    assert game.ourRobots[0].position == (10, board_size)
    assert game.ourRobots[0].damage == 0.04
    assert abs(game.ourRobots[0].actual_velocity) <= 0.00001
    assert abs(game.ourRobots[0].desired_velocity) <= 0.00001
    assert game.ourRobots[0].direction == 0


    game.ourRobots[0].robot._set_velocity = 1
    game.ourRobots[0].actual_velocity = 1
    game.ourRobots[0].desired_velocity = 1

    game.ourRobots[0].direction = 180
    game.ourRobots[0].robot._set_direction = 180
    game.ourRobots[0].position = (1, 10)

    game.advance_round()
    assert game.ourRobots[0].position == (0, 10)
    assert game.ourRobots[0].damage == 0.04
    assert game.ourRobots[0].actual_velocity == 1
    assert game.ourRobots[0].desired_velocity == 1
    assert game.ourRobots[0].direction == 180
    game.advance_round()
    assert game.ourRobots[0].position == (0, 10)
    assert game.ourRobots[0].damage == 0.06
    assert abs(game.ourRobots[0].actual_velocity) <= 0.00001
    assert abs(game.ourRobots[0].desired_velocity) <= 0.00001
    assert game.ourRobots[0].direction == 90


    game.ourRobots[0].robot._set_velocity = 1
    game.ourRobots[0].actual_velocity = 1
    game.ourRobots[0].desired_velocity = 1

    game.ourRobots[0].direction = 270
    game.ourRobots[0].robot._set_direction = 270
    game.ourRobots[0].position = (10, 1)

    game.advance_round()
    assert game.ourRobots[0].position == (10, 0)
    assert game.ourRobots[0].damage == 0.06
    assert game.ourRobots[0].actual_velocity == 1
    assert game.ourRobots[0].desired_velocity == 1
    assert game.ourRobots[0].direction == 270
    game.advance_round()
    assert game.ourRobots[0].position == (10, 0)
    assert game.ourRobots[0].damage == 0.08
    assert abs(game.ourRobots[0].actual_velocity) <= 0.00001
    assert abs(game.ourRobots[0].desired_velocity) <= 0.00001
    assert game.ourRobots[0].direction == 180


    game.ourRobots[0].robot._set_velocity = 1
    game.ourRobots[0].actual_velocity = 1
    game.ourRobots[0].desired_velocity = 1

    game.ourRobots[0].direction = 45
    game.ourRobots[0].robot._set_direction = 45
    game.ourRobots[0].position = (board_size - 1, board_size - 1)

    game.advance_round()
    assert abs(game.ourRobots[0].position[0] - (board_size - 1 + 2**(-1/2))) <= 0.00001
    assert abs(game.ourRobots[0].position[1] - (board_size - 1 + 2**(-1/2))) <= 0.00001
    assert game.ourRobots[0].damage == 0.08
    assert game.ourRobots[0].actual_velocity == 1
    assert game.ourRobots[0].desired_velocity == 1
    assert game.ourRobots[0].direction == 45
    game.advance_round()
    assert game.ourRobots[0].position == (board_size, board_size)
    assert game.ourRobots[0].damage == 0.1
    assert game.ourRobots[0].actual_velocity == 0
    assert game.ourRobots[0].desired_velocity == 0


    game.ourRobots[0].robot._set_velocity = (1/2)**(1/2)
    game.ourRobots[0].actual_velocity = (1/2)**(1/2)
    game.ourRobots[0].desired_velocity = (1/2)**(1/2)

    game.ourRobots[0].direction = 225
    game.ourRobots[0].robot._set_direction = 225
    game.ourRobots[0].position = (10, 0.5)

    game.advance_round()
    assert abs(game.ourRobots[0].position[0] - 9.5) <= 0.00001
    assert abs(game.ourRobots[0].position[1]) <= 0.00001
    assert game.ourRobots[0].damage == 0.1
    assert game.ourRobots[0].actual_velocity == (1/2)**(1/2)
    assert game.ourRobots[0].desired_velocity == (1/2)**(1/2)
    assert game.ourRobots[0].direction == 225
    game.advance_round()
    assert abs(game.ourRobots[0].position[0] - 9) <= 0.00001
    assert game.ourRobots[0].position[1] == 0
    assert abs(game.ourRobots[0].damage - 0.12) <= 0.00001
    assert abs(game.ourRobots[0].actual_velocity - 1/2) <= 0.00001
    assert abs(game.ourRobots[0].desired_velocity - 1/2) <= 0.00001
    assert game.ourRobots[0].direction == 180


def test_invalid_shots():
    import app.tests.robots_for_testing.empty as empty
    game: GameState = GameState(
        [
            ('empty', empty.empty)
        ],
        for_animation=True
    )

    game.ourRobots[0].robot._is_cannon_ready = True
    game.ourRobots[0].robot._is_shooting = True
    game.ourRobots[0].robot._shot_direction = None
    game.ourRobots[0].robot._shot_distance = None

    game.advance_round()
    assert game.future_explosions == []


    game.ourRobots[0].robot.is_cannon_ready = 0
    game.ourRobots[0].robot._is_cannon_ready = True
    game.ourRobots[0].robot._is_shooting = True
    game.ourRobots[0].robot._shot_direction = (lambda x: x+1)
    game.ourRobots[0].robot._shot_distance = 5

    game.advance_round()
    assert game.future_explosions == []

    game.ourRobots[0].robot.is_cannon_ready = 0
    game.ourRobots[0].robot._is_cannon_ready = True
    game.ourRobots[0].robot._is_shooting = True
    game.ourRobots[0].robot._shot_direction = "not a number"
    game.ourRobots[0].robot._shot_distance = "a"

    game.advance_round()
    assert game.future_explosions == []

    #valid shot
    game.ourRobots[0].robot.is_cannon_ready = 0
    game.ourRobots[0].robot._is_cannon_ready = True
    game.ourRobots[0].robot._is_shooting = True
    game.ourRobots[0].robot._shot_direction = 1
    game.ourRobots[0].robot._shot_distance = 1

    game.advance_round()
    assert game.future_explosions != []


def test_explosions():
    import app.tests.robots_for_testing.empty as empty
    game: GameState = GameState(
        [
            ('empty', empty.empty),
            ('empty', empty.empty)
        ],
        for_animation=True
    )

    game.ourRobots[0].position = (100, 100)
    game.ourRobots[1].position = (300, 100)

    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage == 0
    game.advance_round()
    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage == 0

    game.ourRobots[0].robot.cannon(0, 200)
    for _ in range(int(200 // missile_velocity) + 1):
        assert game.ourRobots[0].damage == 0
        assert game.ourRobots[1].damage == 0
        game.advance_round()
    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage == 0.1

    game.ourRobots[1].robot.cannon(180, 200)
    for _ in range(int(200 // missile_velocity) + 1):
        assert game.ourRobots[0].damage == 0
        assert game.ourRobots[1].damage == 0.1
        game.advance_round()
    assert game.ourRobots[0].damage == 0.1
    assert game.ourRobots[1].damage == 0.1

    game.ourRobots[0].robot.cannon(math.atan(2/200) * 180/math.pi, math.sqrt(200**2 + 2**2))
    for _ in range(int(math.sqrt(200**2 + 2**2) // missile_velocity) + 1):
        assert game.ourRobots[0].damage == 0.1
        assert game.ourRobots[1].damage == 0.1
        game.advance_round()
    assert game.ourRobots[0].damage == 0.1
    assert game.ourRobots[1].damage == 0.1 + 0.1

    while game.ourRobots[0].is_cannon_ready > 0 or game.ourRobots[1].is_cannon_ready > 0:
        game.advance_round()

    game.ourRobots[0].robot.cannon(0, 200)
    game.ourRobots[1].robot.cannon(180, 200)
    for _ in range(int(200 // missile_velocity) + 1):
        assert game.ourRobots[0].damage == 0.1
        assert game.ourRobots[1].damage == 0.1 + 0.1
        game.advance_round()
    assert game.ourRobots[0].damage == 0.1 + 0.1
    assert game.ourRobots[1].damage == 0.1 + 0.1 + 0.1

    while game.ourRobots[0].is_cannon_ready > 0 or game.ourRobots[1].is_cannon_ready > 0:
        game.advance_round()

    game.ourRobots[0].robot.cannon(0, 210)
    for _ in range(int(210 // missile_velocity) + 1):
        assert game.ourRobots[0].damage == 0.1 + 0.1
        assert game.ourRobots[1].damage == 0.1 + 0.1 + 0.1
        game.advance_round()
    assert game.ourRobots[0].damage == 0.1 + 0.1
    assert game.ourRobots[1].damage == 0.1 + 0.1 + 0.1 + 0.05

    game.ourRobots[0].robot.cannon(0, 170)
    for _ in range(int(170 // missile_velocity) + 1):
        assert game.ourRobots[0].damage == 0.1 + 0.1
        assert game.ourRobots[1].damage == 0.1 + 0.1 + 0.1 + 0.05
        game.advance_round()
    assert game.ourRobots[0].damage == 0.1 + 0.1
    assert game.ourRobots[1].damage == 0.1 + 0.1 + 0.1 + 0.05 + 0.03


def test_collisions_between_robots():
    import app.tests.robots_for_testing.empty as empty
    game: GameState = GameState(
        [
            ('empty', empty.empty),
            ('empty', empty.empty)
        ],
        for_animation=True
    )

    game.ourRobots[0].position = (100, 100)
    game.ourRobots[1].position = (100, 100)

    game.advance_round()

    assert game.ourRobots[0].damage == 0.2
    assert game.ourRobots[1].damage == 0.2