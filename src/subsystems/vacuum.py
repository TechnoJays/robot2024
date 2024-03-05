from configparser import ConfigParser

from commands2 import Subsystem
from wpilib import PWMVictorSPX, PWMTalonSRX
from wpilib import SmartDashboard


class Vacuum(Subsystem):
    # Config file section names
    GENERAL_SECTION = "VacuumGeneral"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"

    def __init__(
            self,
            config: ConfigParser,
    ):
        self._config = config
        self._init_components()
        super().__init__()

    def _init_components(self):
        self._max_speed = self._config.getfloat(
            Vacuum.GENERAL_SECTION, Vacuum.MAX_SPEED_KEY
        )
        if self._config.getboolean(Vacuum.GENERAL_SECTION, Vacuum.ENABLED_KEY):
            self._motor = PWMTalonSRX(
                self._config.getint(Vacuum.GENERAL_SECTION, Vacuum.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Vacuum.GENERAL_SECTION, Vacuum.INVERTED_KEY)
            )
        Vacuum._update_smartdashboard(0.0)

    def move(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            adjusted_speed = speed * self._max_speed
            self._motor.set(adjusted_speed)
        Vacuum._update_smartdashboard(adjusted_speed)

    @staticmethod
    def _update_smartdashboard(speed: float = 0.0):
        SmartDashboard.putNumber("Vacuum Speed", speed)
