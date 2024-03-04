from robot_controller import RobotController

SUBSYSTEMS_CONFIG_PATH = "../tests/test_configs/subsystems_default.ini"
JOYSTICK_CONFIG_PATH = "../tests/test_configs/joysticks_default.ini"
AUTONOMOUS_CONFIG_PATH = "../tests/test_configs/autonomous_default.ini"


def test__init():
    # given: a robot controller with valid config paths
    controller = RobotController(SUBSYSTEMS_CONFIG_PATH, JOYSTICK_CONFIG_PATH, AUTONOMOUS_CONFIG_PATH)

    # then: all the controllers configs should be initialized
    assert controller.subsystems_config is not None
    assert controller.joystick_config is not None
    assert controller.autonomous_config is not None

    # and all subsystems should be initialized
    assert controller.drivetrain is not None
    assert controller.drivetrain.left_motor is not None
    assert controller.drivetrain.right_motor is not None
    assert controller.oi is not None

    assert controller.vacuum is not None
    assert controller.vacuum._motor is not None

    assert controller.shooter is not None
    assert controller.shooter._motor is not None

    assert controller.climber is not None
    assert controller.climber._motor is not None
