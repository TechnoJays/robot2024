# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser

from commands2 import SubsystemBase
from wpilib import PneumaticsModuleType, Solenoid, SmartDashboard


class Grabber(SubsystemBase):
    # Config file section name
    GENERAL_SECTION = "GrabberGeneral"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    SOLENOID_CHANNEL_KEY = "SOLENOID_CHANNEL"
    SOLENOID_INVERTED_KEY = "SOLENOID_INVERTED"

    def __init__(self, config: ConfigParser):
        super().__init__()
        self._config = config
        self._init_components()

    def _init_components(self) -> None:
        self._enabled = self._config.getboolean(Grabber.GENERAL_SECTION, Grabber.ENABLED_KEY)

        self._channel = self._config.getint(Grabber.GENERAL_SECTION, Grabber.SOLENOID_CHANNEL_KEY)
        self._solenoid = Solenoid(PneumaticsModuleType.CTREPCM, self._channel)
        SmartDashboard.putNumber("Grabber Solenoid DIO Channel", self._solenoid.getChannel())   

    def grab(self):
        if not self._enabled or not self._solenoid:
            return
        self._solenoid.set(True)
        Grabber.update_smartdashboard(self._solenoid.get())

    def release(self):
        if not self._enabled or not self._solenoid:
            return
        self._solenoid.set(False)
        Grabber.update_smartdashboard(self._solenoid.get())

    @staticmethod
    def update_smartdashboard(solenoid_state: bool):
        SmartDashboard.putBoolean("Grabber Solenoid", solenoid_state)

    @property
    def solenoid(self) -> Solenoid:
        return self._solenoid
