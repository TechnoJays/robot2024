from configparser import ConfigParser

import pytest

from commands.tank_drive_commands import GoTurbo, ReleaseTurbo
from oi import OI
from subsystems.drivetrain import Drivetrain


@pytest.fixture(scope="session")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_default.ini")
    return config


@pytest.fixture(scope="session")
def drivetrain_default(config_default: ConfigParser):
    return Drivetrain(config_default)


@pytest.fixture(scope="session")
def joy_config() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/joysticks_default.ini")
    return config


@pytest.fixture(scope="session")
def oi_default(joy_config: ConfigParser):
    oi = OI(joy_config)
    return oi


def test_initialize(drivetrain_default: Drivetrain):
    command = GoTurbo(drivetrain_default)

    assert command._drivetrain == drivetrain_default
    assert not command._turbo_updated


def test_execute(drivetrain_default: Drivetrain):
    command = GoTurbo(drivetrain_default)
    command.execute()

    assert command.turboUpdated()

    assert drivetrain_default._turbo
    assert not drivetrain_default._slow


def test_is_finished(drivetrain_default: Drivetrain):
    command = GoTurbo(drivetrain_default)
    assert not command.isFinished()

    command.execute()
    assert command.isFinished()


def test_get_requirements(drivetrain_default: Drivetrain):
    command = GoTurbo(drivetrain_default)
    assert drivetrain_default in command.getRequirements()


def test_release_initialize(drivetrain_default: Drivetrain):
    command = ReleaseTurbo(drivetrain_default)

    assert command._drivetrain == drivetrain_default
    assert not command._turbo_updated


def test_release_execute(drivetrain_default: Drivetrain):
    command = ReleaseTurbo(drivetrain_default)
    command.execute()

    assert command.turboUpdated()

    assert not drivetrain_default._turbo
    assert not drivetrain_default._slow


def test_release_is_finished(drivetrain_default: Drivetrain):
    command = ReleaseTurbo(drivetrain_default)
    assert not command.isFinished()

    command.execute()
    assert command.isFinished()


def test_release_get_requirements(drivetrain_default: Drivetrain):
    command = ReleaseTurbo(drivetrain_default)
    assert drivetrain_default in command.getRequirements()
