from configparser import ConfigParser

import pytest
from wpilib import IterativeRobotBase
from wpilib.simulation import PWMSim

from commands.arcade_drive_commands import DriveTime
from subsystems.drivetrain import Drivetrain


@pytest.fixture(scope="function")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_default.ini")
    return config


@pytest.fixture(scope="function")
def drivetrain_default(config_default: ConfigParser):
    return Drivetrain(config_default)


@pytest.fixture(scope="function")
def command_default(drivetrain_default: Drivetrain):
    command_default = DriveTime(drivetrain_default, duration=5.0, speed=1.0)
    command_default.setName("TestDriveTime")
    return command_default


def test_init_default(command_default: DriveTime):
    assert command_default is not None
    assert command_default.drivetrain is not None
    assert command_default.stopwatch is not None
    assert command_default.getName() is not None
    assert command_default.duration == 5
    assert command_default.speed == 1.0


def test_init_full(drivetrain_default: Drivetrain):
    dt = DriveTime(drivetrain_default, 10.0, 0.5)
    dt.setName("TestDriveTime")
    assert dt is not None
    assert dt.drivetrain is not None
    assert dt.drivetrain == drivetrain_default
    assert dt.stopwatch is not None
    assert dt.duration == 10
    assert dt.speed == 0.5


def test_initialize(command_default: DriveTime):
    command_default.initialize()
    assert command_default._stopwatch._running


@pytest.mark.parametrize(
    "speed,left_ex_speed,right_ex_speed",
    [
        (0.0, 0.0, 0.0),
        (0.5, 0.4897959183673469, -0.4897959183673469),
        (1.0, 1.0, -1.0),
        (-0.5, -0.5306122448979592, 0.5306122448979592),
        (-1.0, -1.0, 1.0),
    ],
)
def test_execute(
        robot: IterativeRobotBase,
        drivetrain_default: Drivetrain,
        speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    # given: a drivetrain
    robot.drivetrain = drivetrain_default

    # and: left and right motors on the drive train
    left_motor_sim = PWMSim(drivetrain_default._left_motor.getChannel())
    right_motor_sim = PWMSim(drivetrain_default._right_motor.getChannel())

    # and: a command to drive the robot forward for five seconds
    dt = DriveTime(drivetrain_default, 5, speed)

    # when: drive time command is initialized and executed
    dt.initialize()
    dt.execute()

    # then: the speed of both motors should match the speed from the command
    pytest.approx(left_motor_sim.getSpeed(), left_ex_speed)
    pytest.approx(right_motor_sim.getSpeed(), right_ex_speed)


def test_is_finished(command_default: DriveTime):
    command_default.initialize()
    assert command_default.isFinished() is False


def test_interrupted(command_default: DriveTime):
    pass  # interrupted method is empty


def test_end(
        robot: IterativeRobotBase,
        command_default: DriveTime,
        drivetrain_default: Drivetrain,
):
    assert command_default._stopwatch._running is False

    # given: a drivetrain
    robot.drivetrain = drivetrain_default
    # and: left and right motors on the drive train
    left_motor_sim = PWMSim(drivetrain_default._left_motor.getChannel())
    right_motor_sim = PWMSim(drivetrain_default._right_motor.getChannel())

    # then: the speed of both motors should match the speed from the command
    assert 0.0 == pytest.approx(left_motor_sim.getSpeed())
    assert 0.0 == pytest.approx(right_motor_sim.getSpeed())


def is_close(a, b, rel_tol=0.1, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


@pytest.mark.parametrize(
    "duration,speed,left_ex_speed,right_ex_speed",
    [
        (0.5, 0.5, 0.5306122448979592, -0.5306122448979592),
        (1.5, 1.0, 1.0, -1.0),
        (2.0, 1.0, -1.0, 1.0),
    ],
)
def test_command_full(
        drivetrain_default: Drivetrain,
        duration: float,
        speed: float,
        left_ex_speed: float,
        right_ex_speed: float,
):
    # given: a drivetrain (in drivetrain_default)
    assert drivetrain_default is not None

    # and: left and right motors on the drive train
    left_motor_sim = PWMSim(drivetrain_default._left_motor.getChannel())
    right_motor_sim = PWMSim(drivetrain_default._right_motor.getChannel())

    # and: a command to drive with a duration and speed, measured by a stopwatch
    dt = DriveTime(drivetrain_default, duration, speed)

    # when: initializing the command to start
    dt.initialize()

    # and: the command is processed until it is finished
    while not dt.isFinished():
        dt.execute()
        pytest.approx(left_ex_speed, left_motor_sim.getSpeed())
        pytest.approx(right_ex_speed, right_motor_sim.getSpeed())

    # and: the command is ended, uninterrupted
    dt.end(True)

    # then: the elapsed time on the commands internal stopwatch should be close to the duration
    # specified in the command (close because processing time is unpredictable)
    assert is_close(dt.stopwatch.elapsed_time_in_secs(), duration)
