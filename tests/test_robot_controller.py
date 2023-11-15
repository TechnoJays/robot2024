from commands2 import TimedCommandRobot

from robot_controller import RobotController

SUBSYSTEMS_CONFIG_PATH = "../tests/test_configs/subsystems_default.ini"
JOYSTICK_CONFIG_PATH = "../tests/test_configs/joysticks_default.ini"
AUTONOMOUS_CONFIG_PATH = "../tests/test_configs/autonomous_default.ini"


def test__init(robot: TimedCommandRobot):
    # given: a robot controller with valid config paths
    controller = RobotController(robot, SUBSYSTEMS_CONFIG_PATH, JOYSTICK_CONFIG_PATH, AUTONOMOUS_CONFIG_PATH)

    # then: all the controllers configs should be initialized
    assert controller.subsystems_config is not None
    assert controller.joystick_config is not None
    assert controller.autonomous_config is not None

    # and all subsystems should be initialized
    assert controller.drivetrain is not None
    assert controller.drivetrain.left_motor is not None
    assert controller.drivetrain.right_motor is not None
    assert controller.oi is not None

    assert controller.arm is not None
    assert controller.arm._motor is not None

    assert controller.grabber is not None
