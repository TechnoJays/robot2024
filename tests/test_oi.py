from configparser import ConfigParser

import pytest

from autonomous.autonomous_drive_commands import MoveFromLine
from oi import OI
from subsystems.drivetrain import Drivetrain


@pytest.fixture(scope="function")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/joysticks_default.ini")
    return config


@pytest.fixture(scope="function")
def config_joy_ports_01() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/joysticks_ports_0_1.ini")
    return config


@pytest.fixture(scope="function")
def config_auto() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/autonomous_default.ini")
    return config


@pytest.fixture(scope="function")
def oi_default(config_default: ConfigParser) -> OI:
    return OI(config_default)


@pytest.fixture(scope="function")
def oi_joy_ports(config_joy_ports_01: ConfigParser) -> OI:
    return OI(config_joy_ports_01)


@pytest.fixture(scope="function")
def drivetrain_config() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/drivetrain_default.ini")
    return config


@pytest.fixture(scope="function")
def drivetrain_default(drivetrain_config: ConfigParser) -> Drivetrain:
    return Drivetrain(drivetrain_config)


def test__init_joystick(oi_joy_ports: OI, config_joy_ports_01: ConfigParser):
    assert oi_joy_ports is not None
    assert oi_joy_ports.config() == config_joy_ports_01
    assert len(oi_joy_ports.controllers()) == 2
    assert oi_joy_ports.controllers()[0] is not None
    assert oi_joy_ports.controllers()[1] is not None


def test__init_dead_zone(oi_joy_ports: OI, config_joy_ports_01: ConfigParser):
    assert oi_joy_ports is not None
    assert oi_joy_ports.config() == config_joy_ports_01
    assert len(oi_joy_ports.controllers()) == 2
    assert oi_joy_ports.controllers()[0] is not None
    assert oi_joy_ports.controllers()[1] is not None


@pytest.mark.skip(reason="don't know why robot is None for this test")
def test__setup_autonomous_smartdashboard(drivetrain_default: Drivetrain,
                                          oi_default: OI, config_auto: ConfigParser):
    assert oi_default is not None
    auto_chooser = oi_default._setup_autonomous_smartdashboard(drivetrain_default, config_auto)
    assert auto_chooser is not None
    assert type(auto_chooser.getSelected()) is MoveFromLine


@pytest.mark.skip(reason="requires setup_autonomous_dashboard")
def test_get_auto_choice():
    assert False


@pytest.mark.skip(reason="unimplemented for lack of time")
def test_get_position():
    assert False


@pytest.mark.skip(reason="no important game message (panel color) for 2024 game")
def test_get_game_message():
    assert False


@pytest.mark.skip(reason="reserved for later sophisticated pyfrc/robotpy testing")
def test_get_axis():
    assert False


@pytest.mark.skip(reason="reserved for later sophisticated pyfrc/robotpy testing")
def test_get_button_state():
    assert False
