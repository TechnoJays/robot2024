import configparser

from commands2 import SubsystemBase
from wpilib import PneumaticsModuleType
from wpilib import SmartDashboard
from wpilib import Solenoid

from commands.shooter_commands import LowerShooter


class Flipper(SubsystemBase):
    GENERAL_SECTION = "FlipperGeneral"

    ENABLED_KEY = "ENABLED"
    SOLENOID_CHANNEL_KEY = "SOLENOID_CHANNEL"
    SOLENOID_INVERTED_KEY = "SOLENOID_INVERTED"

    _robot = None
    _solenoid: Solenoid = None
    _solenoid_inverted: bool = False
    _enabled: bool = False

    def __init__(
        self, robot, name="Flipper", configfile="/home/lvuser/py/configs/subsystems.ini"
    ):
        self._robot = robot
        self._config = configparser.ConfigParser()
        self._config.read(configfile)
        self._enabled = self._config.getboolean(
            Flipper.GENERAL_SECTION, Flipper.ENABLED_KEY
        )
        self._init_components()
        self.setName(name)
        super().__init__()

    def _init_components(self):
        if self._enabled:
            self._solenoid_inverted = self._config.getboolean(
                Flipper.GENERAL_SECTION, Flipper.SOLENOID_INVERTED_KEY
            )
            self._solenoid = Solenoid(
                PneumaticsModuleType.CTREPCM,
                self._config.getint(
                    Flipper.GENERAL_SECTION, Flipper.SOLENOID_CHANNEL_KEY
                ),
            )

    def initDefaultCommand(self):
        self.setDefaultCommand(LowerShooter(self._robot))

    def upheave(self, state: bool):
        if not self._enabled:
            return
        self._solenoid.set(state ^ self._solenoid_inverted)
        Flipper.update_smartdashboard(self._solenoid.get())

    @staticmethod
    def update_smartdashboard(solenoid: bool):
        SmartDashboard.putBoolean("Flipper Solenoid", solenoid)
