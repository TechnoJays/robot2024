import configparser

from commands2 import SubsystemBase
from wpilib import DigitalInput, IterativeRobotBase
from wpilib import PWMTalonSRX
from wpilib import SmartDashboard

from commands.winch_commands import MoveWinch


class Climbing(SubsystemBase):
    # Config file section names
    GENERAL_SECTION = "ClimbingGeneral"
    LIMIT_SWITCH_SECTION = "ClimbingLimitSwitch"
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

    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = "Winch",
        configfile: str = "/home/lvuser/py/configs/subsystems.ini",
    ):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._init_components()
        self._update_smartdashboard_sensors()
        self.setName(name)
        super().__init__()
        

    def _init_components(self):
        self._max_speed = self._config.getfloat(
            Climbing.GENERAL_SECTION, Climbing.MAX_SPEED_KEY
        )
        if self._config.getboolean(Climbing.GENERAL_SECTION, Climbing.ENABLED_KEY):
            self._motor = PWMTalonSRX(
                self._config.getint(Climbing.GENERAL_SECTION, Climbing.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Climbing.GENERAL_SECTION, Climbing.INVERTED_KEY)
            )
        if self._config.getboolean(Climbing.LIMIT_SWITCH_SECTION, Climbing.ENABLED_KEY):
            self._limit_switch = DigitalInput(
                self._config.getint(Climbing.LIMIT_SWITCH_SECTION, Climbing.CHANNEL_KEY)
            )
            self._limit_switch_inverted = self._config.getboolean(
                Climbing.LIMIT_SWITCH_SECTION, Climbing.INVERTED_KEY
            )

    def initDefaultCommand(self):
        self.setDefaultCommand(MoveWinch(self._robot, "MoveWinch"))

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
