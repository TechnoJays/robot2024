import configparser
import logging

from commands2 import Subsystem
from wpilib import PWMMotorController, PWMVictorSPX, SmartDashboard


class Shooter(Subsystem):
    # Config file section name
    GENERAL_SECTION = "ShooterGeneral"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"

    _enabled: bool = False

    _motor: PWMMotorController = None
    _max_speed: float = 0.0

    def __init__(self, config: configparser.ConfigParser):
        super().__init__()
        self._config = config
        self._init_components()
        logging.info("Shooter initialized")
        # TODO move smartdashboard update to Robot Controller
        Shooter._update_smartdashboard(0.0)

    def _init_components(self):
        self._enabled = self._config.getboolean(
            Shooter.GENERAL_SECTION, Shooter.ENABLED_KEY
        )

        self._max_speed = self._config.getfloat(
            Shooter.GENERAL_SECTION, Shooter.MAX_SPEED_KEY
        )
        if self._enabled:
            logging.debug("Shooter enabled")
            self._motor = PWMVictorSPX(
                self._config.getint(Shooter.GENERAL_SECTION, Shooter.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Shooter.GENERAL_SECTION, Shooter.INVERTED_KEY)
            )

    def move(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            adjusted_speed = speed * self._max_speed
            self._motor.set(adjusted_speed)
        Shooter._update_smartdashboard(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Shooter Speed", speed)
