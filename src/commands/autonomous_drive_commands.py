from configparser import ConfigParser

from commands2 import Command

from commands.arcade_drive_commands import DriveTime
from subsystems.drivetrain import Drivetrain


class MoveFromLine(Command):
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
            self.andThen(command)
        else:
            print('Drivetrain not found for MoveLine')
