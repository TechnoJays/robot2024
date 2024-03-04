from configparser import ConfigParser

from commands2 import Subsystem
from wpilib import PWMTalonSRX
from wpilib import SmartDashboard


class Climber(Subsystem):
    # Config file section names
    GENERAL_SECTION = "ClimberGeneral"
    LIMIT_SWITCH_SECTION = "ClimberLimitSwitch"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    CHANNEL_KEY = "CHANNEL"
    MAX_SPEED_KEY = "MAX_SPEED"

    _max_speed = 0

    _robot = None
    _config = None
    _motor = None

    _limit_switch = None
    _limit_switch_inverted = False

    def __init__(self, config: ConfigParser):
        super().__init__()
        self._config = config
        self._init_components()
        # TODO refactor smartdashboard updates to robot_controller
        self._update_smartdashboard_sensors()

    def _init_components(self):
        self._max_speed = self._config.getfloat(
            Climber.GENERAL_SECTION, Climber.MAX_SPEED_KEY
        )

        if self._config.getboolean(Climber.GENERAL_SECTION, Climber.ENABLED_KEY):
            self._motor = PWMTalonSRX(
                self._config.getint(Climber.GENERAL_SECTION, Climber.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Climber.GENERAL_SECTION, Climber.INVERTED_KEY)
            )

    def is_retracted(self) -> bool:
        return self._limit_switch_inverted ^ self._limit_value()

    def _limit_value(self) -> bool:
        if self._limit_switch is not None:
            return self._limit_switch.get()
        else:
            return False

    def _update_smartdashboard_sensors(self, speed: float = 0.0):
        SmartDashboard.putNumber("Winch Speed", speed)
        if self._limit_switch is not None:
            SmartDashboard.putBoolean("Winch Retracted", self.is_retracted())
            SmartDashboard.putBoolean("Winch Limit Switch State", self._limit_value())

    def move_winch(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            if speed < 0.0:
                adjusted_speed = speed * self._max_speed
            elif speed > 0.0 and not self.is_retracted():
                adjusted_speed = speed * self._max_speed
            else:
                adjusted_speed = 0.0
            self._motor.set(adjusted_speed)
        self._update_smartdashboard_sensors(adjusted_speed)

    def potentiometer_raw(self) -> float:
        return 0.0
