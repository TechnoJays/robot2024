# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser

import pytest
from wpilib import PWMTalonSRX, AnalogPotentiometer

from subsystems.climber import Climber


@pytest.fixture(scope="function")
def config_default() -> ConfigParser:
    config = ConfigParser()
    config.read("./test_configs/subsystems_default.ini")
    return config


def test__init_components(config_default: ConfigParser):
    climber = Climber(config_default)
    assert climber._config
    assert climber._max_speed == config_default.getfloat(Climber.GENERAL_SECTION, Climber.MAX_SPEED_KEY)
    assert isinstance(climber._motor, PWMTalonSRX)
    assert not climber._motor.getInverted()

    assert climber._pot_channel == 2
    assert climber._pot_full_range == 3600
    assert climber._pot_retracted_threshold == -1575
    assert climber._pot_extended_threshold == 1530
    assert isinstance(climber._pot_limiter, AnalogPotentiometer)


def test_is_retracted(config_default: ConfigParser):
    climber = Climber(config_default)
    

@pytest.mark.skip(reason="Need to get pyfrc/sim working")
def test_is_extended():
    assert False

@pytest.mark.skip(reason="Need to get pyfrc/sim working")
def test__update_smartdashboard_sensors():
    assert False

@pytest.mark.skip(reason="Need to get pyfrc/sim working")
def test_move_winch():
    assert False

@pytest.mark.skip(reason="Need to get pyfrc/sim working")
def test_potentiometer():
    assert False
