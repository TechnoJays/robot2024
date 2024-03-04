# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser

import pytest
from commands2 import Command
from wpilib.simulation import PWMSim

import oi
from commands.tank_drive_commands import TankDrive
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
def mock_oi():
    class OI:
        driver_axis_values = {
            oi.JoystickAxis.LEFTX: 0.0,
            oi.JoystickAxis.LEFTY: 0.0,
            oi.JoystickAxis.RIGHTX: 0.0,
            oi.JoystickAxis.RIGHTY: 0.0,
            oi.JoystickAxis.DPADX: 0.0,
            oi.JoystickAxis.DPADY: 0.0,
        }
        scoring_axis_values = {
            oi.JoystickAxis.LEFTX: 0.0,
            oi.JoystickAxis.LEFTY: 0.0,
            oi.JoystickAxis.RIGHTX: 0.0,
            oi.JoystickAxis.RIGHTY: 0.0,
            oi.JoystickAxis.DPADX: 0.0,
            oi.JoystickAxis.DPADY: 0.0,
        }
        axis_values = {
            oi.UserController.DRIVER: driver_axis_values,
            oi.UserController.SCORING: scoring_axis_values,
        }

        driver_button_values = {
            oi.JoystickButtons.A: False,
            oi.JoystickButtons.B: False,
            oi.JoystickButtons.X: False,
            oi.JoystickButtons.Y: False,
            oi.JoystickButtons.BACK: False,
            oi.JoystickButtons.START: False,
            oi.JoystickButtons.LEFTBUMPER: False,
            oi.JoystickButtons.RIGHTBUMPER: False,
            oi.JoystickButtons.LEFTTRIGGER: False,
            oi.JoystickButtons.RIGHTTRIGGER: False,
        }
        scoring_button_values = {
            oi.JoystickButtons.A: False,
            oi.JoystickButtons.B: False,
            oi.JoystickButtons.X: False,
            oi.JoystickButtons.Y: False,
            oi.JoystickButtons.BACK: False,
            oi.JoystickButtons.START: False,
            oi.JoystickButtons.LEFTBUMPER: False,
            oi.JoystickButtons.RIGHTBUMPER: False,
            oi.JoystickButtons.LEFTTRIGGER: False,
            oi.JoystickButtons.RIGHTTRIGGER: False,
        }
        button_values = {
            oi.UserController.DRIVER: driver_button_values,
            oi.UserController.SCORING: scoring_button_values,
        }

        def set_mock_axis_value(self, controller, axis, value):
            self.axis_values[controller][axis] = value

        def get_axis(self, controller, axis):
            return self.axis_values[controller][axis]

        def set_mock_button_value(self, controller, button, value):
            self.button_values[controller][button] = value

        def get_button_state(self, user, button):
            return self.button_values[user][button]

    return OI()


@pytest.fixture(scope="function")
def command_default(mock_oi: oi.OI, drivetrain_default: Drivetrain):
    tank_drive = TankDrive(mock_oi, drivetrain_default)
    tank_drive.setName("TestTankDrive")
    return tank_drive


def test_init_default(command_default: TankDrive, mock_oi: oi.OI, drivetrain_default: Drivetrain):
    assert command_default is not None
    assert command_default.oi is not None
    assert command_default.oi == mock_oi
    assert command_default.drivetrain is not None
    assert command_default.drivetrain == drivetrain_default


def test_init_full(mock_oi: oi.OI, drivetrain_default: Drivetrain):
    td = TankDrive(mock_oi, drivetrain_default)
    assert td is not None
    assert td.drivetrain is not None


def test_initialize(command_default: Command):
    pass  # initialize method is empty


@pytest.mark.parametrize(
    "stick_scale,dpad_scale,left_input,right_input,dpad_input,modifier_input,left_ex_speed,right_ex_speed",
    [
        (1.0, 1.0, 0.0, 0.0, 0.0, False, 0.0, 0.0),
        (1.0, 1.0, 0.5, 0.5, 0.0, False, 0.5306122448979592, -0.5306122448979592),
        (1.0, 1.0, 1.0, 1.0, 0.0, False, 1.0, -1.0),
        (1.0, 1.0, -0.5, -0.5, 0.0, False, -0.5306122448979592, 0.5306122448979592),
        (1.0, 1.0, -1.0, -1.0, 0.0, False, -1.0, 1.0),
        (0.5, 0.5, 0.0, 0.0, 0.0, True, 0.0, 0.0),
        (0.5, 0.5, 0.5, 0.5, 0.0, False, 0.5306122448979592, -0.5306122448979592),
        (0.5, 0.5, 1.0, 1.0, 0.0, True, 0.5306122448979592, -0.5306122448979592),
        (0.5, 0.5, -0.5, -0.5, 0.0, False, -0.5306122448979592, 0.5306122448979592),
        (0.5, 0.5, -1.0, -1.0, 0.0, True, -0.5306122448979592, 0.5306122448979592),
        (1.0, 1.0, 0.0, 0.0, 0.0, False, 0.0, 0.0),
        (1.0, 1.0, 0.5, 0.5, 1.0, False, 1.0, -1.0),
        (1.0, 1.0, 1.0, 1.0, 1.0, False, 1.0, -1.0),
        (1.0, 1.0, -0.5, -0.5, -1.0, False, -1.0, 1.0),
        (1.0, 1.0, -1.0, -1.0, -1.0, False, -1.0, 1.0),
        (0.5, 0.5, 0.0, 0.0, 0.0, True, 0.0, 0.0),
        (0.5, 0.5, 0.5, 0.5, 1.0, False, 0.2815493544356518, -0.2815493544356518),
        (0.5, 0.5, 1.0, 1.0, 1.0, True, 0.2815493544356518, -0.2815493544356518),
        (0.5, 0.5, -0.5, -0.5, -1.0, False, -0.2815493544356518, 0.2815493544356518),
        (0.5, 0.5, -1.0, -1.0, -1.0, True, -0.2815493544356518, 0.2815493544356518),
    ],
)
def test_execute(
        mock_oi,
        drivetrain_default: Drivetrain,
        stick_scale: float,
        dpad_scale: float,
        left_input: float,
        right_input: float,
        dpad_input: float,
        modifier_input: bool,
        left_ex_speed: float,
        right_ex_speed: float,
):
    td = TankDrive(mock_oi, drivetrain_default)
    assert td is not None

    td.initialize()

    mock_oi.set_mock_axis_value(
        oi.UserController.DRIVER, oi.JoystickAxis.LEFTY, left_input
    )
    mock_oi.set_mock_axis_value(
        oi.UserController.DRIVER, oi.JoystickAxis.RIGHTY, right_input
    )
    mock_oi.set_mock_axis_value(
        oi.UserController.DRIVER, oi.JoystickAxis.DPADY, dpad_input
    )
    mock_oi.set_mock_button_value(
        oi.UserController.DRIVER, oi.JoystickButtons.LEFTTRIGGER, modifier_input
    )

    # and: the robot drive motors are real
    left_m = PWMSim(drivetrain_default._left_motor.getChannel())
    right_m = PWMSim(drivetrain_default._right_motor.getChannel())

    td.execute()
    pytest.approx(left_ex_speed, left_m.getSpeed())
    pytest.approx(right_ex_speed, right_m.getSpeed())


def test_is_finished(command_default: TankDrive):
    assert command_default.isFinished() is False


def test_interrupted(command_default: TankDrive):
    pass  # interrupted method is empty


def test_end(command_default: TankDrive):
    pass  # end method is empty
