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
    result_for_animation: RobotResult = robot.get_result_for_animation()
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

    position3 = robot.position # for later

    robot.updateOurRobot_movement(velocity=0.1, direction=135)

    assert robot.name == 'empty'
    assert robot.cause_of_death == None
    assert robot.damage == 0     # When collisions are implemented, this may change
    assert robot.direction == 135
    assert robot.actual_velocity == 0.1
    assert robot.desired_velocity == 0.1
    assert abs(robot.position[0] - (position3[0] - math.cos(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors
    assert abs(robot.position[1] - (position3[1] + math.sin(math.pi/4) * 0.2)) < 0.00001 # There may be rounding errors

    json_output = result_for_animation.json_output()

    assert json_output == {
        'name': 'empty',
        'rounds': [
            { 'coords': {'x': position[0], 'y': position[1] }, 'direction': 0, 'speed': 0 },
            { 'coords': {'x': position[0], 'y': position[1] }, 'direction': 0, 'speed': 0 },
            { 'coords': {'x': position2[0], 'y': position2[1] }, 'direction': 0, 'speed': 0.1 },
            { 'coords': {'x': position3[0], 'y': position3[1] }, 'direction': 135, 'speed': 0.3 },
            { 'coords': {'x': robot.position[0], 'y': robot.position[1] }, 'direction': 135, 'speed': 0.1 }
        ]
    }

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

    assert robot.get_result_for_animation() == None


def testExceptions_RobotInGame():
    import app.tests.robots_for_testing.exception_init as exception_init

    robot: RobotInGame = RobotInGame(exception_init.exception_init, 'exception_init', False)

    assert robot.name == 'exception_init'
    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1

    assert robot.get_result_for_animation() == None

def testExceptions2_RobotInGame():
    import app.tests.robots_for_testing.exception_initialize as exception_initialize

    robot: RobotInGame = RobotInGame(exception_initialize.exception_initialize, 'exception_initialize', False)

    assert robot.name == 'exception_initialize'
    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1

    assert robot.get_result_for_animation() == None

def testExceptions3_RobotInGame():
    import app.tests.robots_for_testing.exception_respond as exception_respond

    robot: RobotInGame = RobotInGame(exception_respond.exception_respond, 'exception_respond', False)

    assert robot.name == 'exception_respond'

    assert robot.cause_of_death == None
    assert robot.damage == 0

    robot.executeRobotCode()

    assert robot.cause_of_death == "robot execution error"
    assert robot.damage == 1

    assert robot.get_result_for_animation() == None

def testInvalidDrives_RobotInGame():
    import app.tests.robots_for_testing.invalid_drives as invalid_drives

    robot: RobotInGame = RobotInGame(invalid_drives.invalid_drives, 'invalid_drives', False)

    assert robot.name == 'invalid_drives'
    assert robot.cause_of_death == None
    assert robot.damage == 0

    robot.executeRobotCode()
    robot.executeRobotCode()
    robot.executeRobotCode()
    robot.executeRobotCode()

    assert robot.name == 'invalid_drives'
    assert robot.cause_of_death == None
    assert robot.damage == 0

    robot.updateOurRobot_movement(-3, 365)
    robot.updateOurRobot_movement(100, 365)

    assert robot.get_result_for_animation() == None

def testGameState():
    import app.tests.robots_for_testing.empty as empty
    import app.tests.robots_for_testing.simple as simple
    import app.tests.robots_for_testing.exception_init as exception_init
    import app.tests.robots_for_testing.exception_respond as exception_respond

    game: GameState = GameState(
        { 
            'empty': empty.empty,
            'simple': simple.simple,
            'exception_init': exception_init.exception_init,
            'exception_respond': exception_respond.exception_respond
        },
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

    game.advance_round()

    assert game.round == 1

    assert game.ourRobots[0].cause_of_death == None
    assert game.ourRobots[1].cause_of_death == None # NOTE: when adding collisions these may change
    assert game.ourRobots[2].cause_of_death == "robot execution error"
    assert game.ourRobots[3].cause_of_death == "robot execution error"

    assert game.ourRobots[0].damage == 0
    assert game.ourRobots[1].damage == 0
    assert game.ourRobots[2].damage == 1
    assert game.ourRobots[3].damage == 1

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

    assert simulationResult == [0, 1]

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
    assert simulationResult.robots[1].cause_of_death == None # NOTE: when adding collisions these may change
    assert simulationResult.robots[2].cause_of_death == "robot execution error"
    assert simulationResult.robots[3].cause_of_death == None

def test_scanner_invalid():
    import app.tests.robots_for_testing.scan_invalid as scan_invalid
    game: GameState = GameState(
        { 
            'scan_invalid': scan_invalid.scan_invalid
        },
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
        { 
            'scan': scan.scan,
            'empty': empty.empty
        },
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



