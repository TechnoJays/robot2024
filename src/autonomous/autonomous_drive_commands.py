import logging
from configparser import ConfigParser

from commands2 import SequentialCommandGroup, WaitCommand

from commands.tank_drive_commands import TankDriveTime
from subsystems.drivetrain import Drivetrain


class MoveFromLine(SequentialCommandGroup):
    _SECTION = "MoveFromLine"
    _DRIVE_SPEED = "DRIVE_SPEED"
    _DRIVE_TIME = "DRIVE_TIME"

    def __init__(
            self,
            drivetrain: Drivetrain,
            auto_config: ConfigParser,
    ):
        """Constructor"""
        super().__init__()
        self._config = auto_config
        self._drivetrain = drivetrain
        self._load_config(auto_config)
        self._initialize_commands(drivetrain)
        logging.info(f"Initialized Move from Line: Drivetrain {drivetrain}")

    def _load_config(self, parser: ConfigParser):
        self._drive_speed = parser.getfloat(self._SECTION, self._DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self._DRIVE_TIME)

    def _initialize_commands(self, drivetrain: Drivetrain) -> None:
        if drivetrain:
            self.addCommands(TankDriveTime(drivetrain, self._drive_time, self._drive_speed))
            logging.info(f"Added TankDriveTime to autonomous: DT={self._drive_time}:, DS={self._drive_speed}")
        else:
            logging.info('Drivetrain not found for MoveLine')


class DelayedMoveFromLine(SequentialCommandGroup):
    _SECTION = "DelayedMoveFromLine"
    WAIT_TIME_KEY = "WAIT_TIME"
    DRIVE_SPEED = "DRIVE_SPEED"
    DRIVE_TIME = "DRIVE_TIME"

    def __init__(
            self,
            drivetrain: Drivetrain,
            auto_config: ConfigParser,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._config = auto_config
        self._load_config(auto_config)
        self._initialize_commands(drivetrain)
        logging.info(f'Initialized Delayed Move from Line: Drivetrain {drivetrain}')

    def _load_config(self, parser: ConfigParser):
        self._wait_time = parser.getfloat(self._SECTION, self.WAIT_TIME_KEY)
        self._drive_speed = parser.getfloat(self._SECTION, self.DRIVE_SPEED)
        self._drive_time = parser.getfloat(self._SECTION, self.DRIVE_TIME)

    def _initialize_commands(self, drivetrain: Drivetrain) -> None:
        if drivetrain:
            self.addCommands(WaitCommand(self._wait_time))
            self.addCommands(TankDriveTime(drivetrain, self._drive_time, self._drive_speed))
            logging.info('Drivetrain found for DelayedMoveFromLine')
        else:
            logging.info('Drivetrain not found for DelayedMoveFromLine')
