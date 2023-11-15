from configparser import ConfigParser

from commands2 import CommandGroupBase
from wpilib import IterativeRobotBase

from commands.arcade_drive_commands import DriveTime
from subsystems.drivetrain import Drivetrain


class MoveFromLine(CommandGroupBase):
    _SECTION = "MoveFromLine"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    _drivetrain: Drivetrain = None

    def __init__(
            self,
            drivetrain: Drivetrain,
            config: ConfigParser,
    ):
        """Constructor"""
        super().__init__()
        self._config = config
        self._load_config(config)
        self._initialize_commands(drivetrain)
        print('move from line: drivetrain - ' + drivetrain)
        self._drivetrain = drivetrain

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self, drivetrain: Drivetrain) -> None:
        if drivetrain:
            command = DriveTime(drivetrain, self._drive_time, self._drive_speed)
            self.addSequential(command)
        else:
            print('Drivetrain not found for MoveLine')


class DriveToWall(CommandGroupBase):
    _SECTION = "DriveToWall"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    _robot = None

    _drive_speed: float = None
    _drive_time: float = None

    def __init__(
            self, robot: IterativeRobotBase, config: ConfigParser,
    ):
        """Constructor"""
        super().__init__()
        self._robot = robot
        self._config = ConfigParser()
        self._load_config(config)
        self._initialize_commands()

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self):
        command = DriveTime(self._robot, self._drive_time, self._drive_speed)
        self.addSequential(command)
