from configparser import ConfigParser

from commands2.button import CommandXboxController
from wpilib import MotorControllerGroup, SendableChooser, PWMTalonSRX, PWMSparkMax, AnalogPotentiometer

from commands.do_nothing import DoNothing
from oi import OI
from robot_controller import RobotController
from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter
from subsystems.vacuum import Vacuum

SUBSYSTEMS_CONFIG_PATH = "../tests/test_configs/subsystems_default.ini"
JOYSTICK_CONFIG_PATH = "../tests/test_configs/joysticks_default.ini"
AUTONOMOUS_CONFIG_PATH = "../tests/test_configs/autonomous_default.ini"


def test__init():
    # given: a robot controller with valid config paths
    controller = RobotController(SUBSYSTEMS_CONFIG_PATH, JOYSTICK_CONFIG_PATH, AUTONOMOUS_CONFIG_PATH)

    # then: all the controllers configs should be initialized
    assert isinstance(controller.subsystems_config, ConfigParser)
    assert isinstance(controller.joystick_config, ConfigParser)
    assert isinstance(controller.autonomous_config, ConfigParser)

    # and all subsystems should be initialized
    assert isinstance(controller.drivetrain, Drivetrain)
    assert isinstance(controller.drivetrain.left_motor, MotorControllerGroup)
    assert isinstance(controller.drivetrain.right_motor, MotorControllerGroup)

    assert isinstance(controller.oi, OI)
    assert isinstance(controller.oi.driver_controller, CommandXboxController)
    assert isinstance(controller.oi.scoring_controller, CommandXboxController)
    assert controller.oi.config() is controller.joystick_config

    assert isinstance(controller.oi.auto_chooser(), SendableChooser)
    assert isinstance(controller.oi.auto_chooser().getSelected(), DoNothing)

    assert isinstance(controller.vacuum, Vacuum)
    assert controller.vacuum._config is controller.subsystems_config
    assert isinstance(controller.vacuum._motor, PWMTalonSRX)
    assert not controller.vacuum._motor.getInverted()
    assert controller.vacuum._max_speed > 0.0

    assert isinstance(controller.shooter, Shooter)
    assert controller.shooter._config is controller.subsystems_config
    assert isinstance(controller.shooter._motor, PWMSparkMax)
    assert not controller.shooter._motor.getInverted()
    assert controller.shooter._max_speed > 0.0

    assert isinstance(controller.climber, Climber)
    assert controller.climber._config is controller.subsystems_config
    assert isinstance(controller.climber._motor, PWMTalonSRX)
    assert not controller.climber._motor.getInverted()
    assert controller.climber._max_speed > 0.0

    assert isinstance(controller.climber.potentiometer(), AnalogPotentiometer)
    assert isinstance(controller.climber.pot_range(), int)
    assert isinstance(controller.climber.pot_offset(), int)
    assert isinstance(controller.climber._pot_retracted_threshold, float)
    assert isinstance(controller.climber._pot_extended_threshold, float)
