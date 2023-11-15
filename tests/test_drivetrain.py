from configparser import ConfigParser

import pytest
from wpilib.simulation import PWMSim

from subsystems.drivetrain import Drivetrain


@pytest.fixture(scope="function")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_default.ini")
    return config


@pytest.fixture(scope="function")
def config_channels_01() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_channels_0_1.ini")
    return config


@pytest.fixture(scope="function")
def config_zero_speed() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_zero_speed.ini")
    return config


@pytest.fixture(scope="function")
def config_half_speed() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_half_speed.ini")
    return config


@pytest.fixture(scope="function")
def config_3_4_speed() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_3_4_speed.ini")
    return config


@pytest.fixture(scope="function")
def config_full_speed() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_full_speed.ini")
    return config


@pytest.fixture(scope="function")
def config_left_inverted() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_left_inverted.ini")
    return config


@pytest.fixture(scope="function")
def config_right_inverted() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_right_inverted.ini")
    return config


@pytest.fixture(scope="function")
def config_left_disabled() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_left_disabled.ini")
    return config


@pytest.fixture(scope="function")
def config_right_disabled() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_right_disabled.ini")
    return config


@pytest.fixture(scope="function")
def drivetrain_default(config_default: ConfigParser):
    return Drivetrain(config_default)


@pytest.fixture(scope="function")
def drivetrain_channels_01(config_channels_01: ConfigParser):
    return Drivetrain(config_channels_01)


@pytest.fixture(scope="function")
def drivetrain_zero_speed(config_zero_speed: ConfigParser):
    return Drivetrain(config_zero_speed)


def test_drivetrain_default(drivetrain_default: Drivetrain):
    assert drivetrain_default is not None
    assert drivetrain_default.left_motor is not None
    assert drivetrain_default.right_motor is not None
    assert drivetrain_default.robot_drive is not None
    # No gyro for 2022
    assert drivetrain_default.is_gyro_enabled() is False
    assert drivetrain_default.arcade_rotation_modifier == -1


def test_drivetrain_channels_0_1(drivetrain_channels_01: Drivetrain):
    # given: a drivetrain with motors connected to channels 0 and 1
    dt = drivetrain_channels_01

    # then: the drivetrain should be valid, and there should be a left and right motor
    assert dt is not None
    assert dt._left_motor is not None
    assert dt._right_motor is not None
    assert dt._robot_drive is not None

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # then: left motor is initialized and zero latched
    assert left_m.getInitialized() is True
    assert left_m.getRawValue() == 0.0
    # Determine how to check this accurately. Check safety enabled? What is zero latch?
    assert left_m.getZeroLatch() is False

    # and: right motor is initialized and zero latched
    assert right_m.getInitialized() is True
    assert right_m.getRawValue() == 0.0
    # Determine how to check this accurately. Check safety enabled? What is zero latch?
    assert right_m.getZeroLatch() is False


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.0, 0.0),
        (1.0, 1.0, 0.0, 0.0),
        (-0.5, -0.5, 0.0, 0.0),
        (-1.0, -1.0, 0.0, 0.0),
    ],
)
def test_drivetrain_zero_speed(
        config_zero_speed: ConfigParser,
        left_speed: float,
        right_speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(config_zero_speed)

    # then: the drivetrain should be valid, and there should be motors
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is not None
    assert dt.max_speed == 0.0

    # and: the robot drive motors are real
    left_m = PWMSim(dt.left_motor.getChannel())
    right_m = PWMSim(dt.right_motor.getChannel())

    # and: the drivetrain is "tank drive" at the left and right speed
    dt.tank_drive(left_speed, right_speed)

    # the speed of the left and right motor should be as set
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.25, -0.25),
        (1.0, 1.0, 0.5, -0.5),
        (-0.5, -0.5, -0.25, 0.25),
        (-1.0, -1.0, -0.5, 0.5),
    ],
)
def test_drivetrain_half_speed(
        config_half_speed: ConfigParser,
        left_speed: float,
        right_speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(config_half_speed)

    # then: the drivetrain should have a left and right motor with a max speed of 0.5
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is not None
    assert dt.max_speed == 0.5

    # and: the robot drive motors are real
    left_m = PWMSim(dt.left_motor.getChannel())
    right_m = PWMSim(dt.right_motor.getChannel())

    # and the drivetrain is "tank drive" at the left right
    dt.tank_drive(left_speed, right_speed)

    # the speed of the left and right motor should be less than it was
    assert abs(left_m.getSpeed()) - abs(left_ex_speed) < 0.05
    assert abs(right_m.getSpeed()) - abs(right_ex_speed) < 0.05


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.375, -0.375),
        (1.0, 1.0, 0.75, -0.75),
        (-0.5, -0.5, -0.375, 0.375),
        (-1.0, -1.0, -0.75, 0.75),
    ],
)
def test_drivetrain_3_4_speed(
        config_3_4_speed: ConfigParser,
        left_speed: float,
        right_speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(config_3_4_speed)

    # then: the drivetrain should have a left and right motor and 3/4 max speed
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is not None
    assert dt.max_speed == 0.75

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # and the drivetrain is "tank drive" at the left right
    dt.tank_drive(left_speed, right_speed)

    # then: the speed of the left and right motor should be less than 0.5
    assert abs(left_m.getSpeed()) - abs(left_ex_speed) < 0.05
    assert abs(right_m.getSpeed()) - abs(right_ex_speed) < 0.05


@pytest.mark.parametrize(
    "left_speed,right_speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0, 0.0),
        (0.5, 0.5, 0.5306122448979592, -0.5306122448979592),
        (1.0, 1.0, 1.0, -1.0),
        (-0.5, -0.5, -0.5306122448979592, 0.5306122448979592),
        (-1.0, -1.0, -1.0, 1.0),
    ],
)
def test_drivetrain_full_speed(
        config_full_speed: ConfigParser,
        left_speed: float,
        right_speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    # given: a drivetrain
    dt = Drivetrain(config_full_speed)

    # then: the drivetrain should have a left and right motor at full speed
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is not None
    assert dt.max_speed == 1.0

    # and: the robot drive motors are real
    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    # and the drivetrain is "tank drive" at the left right
    dt.tank_drive(left_speed, right_speed)

    # then the speed of the left and the right motor should be the speed
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


def test_drivetrain_left_inverted(config_left_inverted: ConfigParser):
    dt = Drivetrain(config_left_inverted)
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is not None

    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    assert left_m.getInitialized() is True
    assert left_m.getSpeed() == 0.0
    assert left_m.getZeroLatch() is False
    assert right_m.getInitialized() is True
    assert right_m.getSpeed() == 0.0
    assert right_m.getZeroLatch() is False
    assert dt._left_motor.getInverted() is True
    assert dt._right_motor.getInverted() is False


def test_drivetrain_right_inverted(config_right_inverted: ConfigParser):
    dt = Drivetrain(config_right_inverted)
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is not None

    left_m = PWMSim(dt._left_motor.getChannel())
    right_m = PWMSim(dt._right_motor.getChannel())

    assert left_m.getInitialized() is True
    assert left_m.getSpeed() == 0.0
    assert left_m.getZeroLatch() is False
    assert right_m.getInitialized() is True
    assert right_m.getSpeed() == 0.0
    assert right_m.getZeroLatch() is False

    assert dt.left_motor.getInverted() is False
    assert dt.right_motor.getInverted() is True


@pytest.mark.skip(reason="how to check disabled")
def test_drivetrain_left_disabled(config_left_disabled: ConfigParser):
    dt = Drivetrain(config_left_disabled)
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is None


@pytest.mark.skip(reason="how to check disabled")
def test_drivetrain_right_disabled(config_right_disabled: ConfigParser):
    dt = Drivetrain(config_right_disabled)
    assert dt is not None
    assert dt.left_motor is not None
    assert dt.right_motor is not None
    assert dt.robot_drive is None


@pytest.mark.skip(reason="implement later")
def test_get_arcade_rotation_modifier():
    assert False


@pytest.mark.skip(reason="implement later")
def test_tank_drive():
    assert False


@pytest.mark.skip(reason="implement later")
def test_arcade_drive():
    assert False


@pytest.mark.skip(reason="implement later")
def test__modify_turn_angle():
    assert False


@pytest.mark.skip(reason="implement later")
def test__init_components():
    assert False
