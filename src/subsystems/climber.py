from configparser import ConfigParser

from commands2 import Subsystem
from wpilib import PWMTalonSRX, AnalogPotentiometer
from wpilib import SmartDashboard


class Climber(Subsystem):
    # Config file section names
    GENERAL_SECTION = "ClimberGeneral"
    CLIMBER_LIMITS_SECTION = "ClimberLimits"
    ENABLED_KEY = "ENABLED"
    MAX_SPEED_KEY = "MAX_SPEED"
    CHANNEL_KEY = "CHANNEL"
    INVERTED_KEY = "INVERTED"
    FULL_RANGE_KEY = "FULL_RANGE"
    OFFSET_RANGE_KEY = "OFFSET"
    EXTENDED_THRESHOLD_KEY = "EXTENDED_THRESHOLD"
    RETRACTED_THRESHOLD_KEY = "RETRACTED_THRESHOLD"

    def __init__(self, config: ConfigParser):
        super().__init__()
        self._config = config
        self._init_components()
        # TODO refactor smartdashboard updates to robot_controller
        self._update_smartdashboard_sensors()

    def _init_components(self):
        self._max_speed = self._config.getfloat(Climber.GENERAL_SECTION, Climber.MAX_SPEED_KEY)

        if self._config.getboolean(Climber.GENERAL_SECTION, Climber.ENABLED_KEY):
            self._motor = PWMTalonSRX(self._config.getint(Climber.GENERAL_SECTION, Climber.CHANNEL_KEY))
            self._motor.setInverted(self._config.getboolean(Climber.GENERAL_SECTION, Climber.INVERTED_KEY))

        if self._config.getboolean(Climber.CLIMBER_LIMITS_SECTION, Climber.ENABLED_KEY):
            self._pot_channel = self._config.getint(Climber.CLIMBER_LIMITS_SECTION, Climber.CHANNEL_KEY)
            self._pot_full_range = self._config.getint(Climber.CLIMBER_LIMITS_SECTION, Climber.FULL_RANGE_KEY)
            self._pot_offset = self._config.getint(Climber.CLIMBER_LIMITS_SECTION, Climber.OFFSET_RANGE_KEY)
            self._pot_retracted_threshold = self._config \
                .getfloat(Climber.CLIMBER_LIMITS_SECTION, Climber.RETRACTED_THRESHOLD_KEY)
            self._pot_extended_threshold = self._config \
                .getfloat(Climber.CLIMBER_LIMITS_SECTION, Climber.EXTENDED_THRESHOLD_KEY)
            self._pot_limiter = AnalogPotentiometer(self._pot_channel, self._pot_full_range, self._pot_offset)

    def is_retracted(self) -> bool:
        return self.potentiometer().get() < self._pot_retracted_threshold

    def is_extended(self) -> bool:
        return self.potentiometer().get() > self._pot_extended_threshold

    def _update_smartdashboard_sensors(self, speed: float = 0.0):
        SmartDashboard.putNumber("Winch Speed", speed)
        if self._pot_limiter is not None:
            SmartDashboard.putNumber("Winch Potentiometer Position", self.potentiometer().get())

    def move_winch(self, speed: float):
        adjusted_speed = 0.0
        if self._motor:
            if speed < 0.0 and not self.is_retracted():
                adjusted_speed = speed * self._max_speed
            elif speed > 0.0 and not self.is_extended():
                adjusted_speed = speed * self._max_speed
            else:
                adjusted_speed = 0.0
            if self.is_climber_between_limits():
                self._motor.set(adjusted_speed)
        self._update_smartdashboard_sensors(adjusted_speed)

    def potentiometer(self) -> AnalogPotentiometer:
        return self._pot_limiter

    def pot_range(self) -> float:
        return self._pot_full_range

    def pot_offset(self) -> float:
        return self._pot_offset

    def is_climber_between_limits(self):
        return self._pot_retracted_threshold < self._pot_limiter.get() < self._pot_extended_threshold
