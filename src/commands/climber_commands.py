from datetime import datetime

from commands2 import Command
from commands2 import Subsystem
from wpilib import IterativeRobotBase

from oi import OI
from subsystems.climber import Climber


class FullWinchRetraction(Command):
    _robot: IterativeRobotBase = None

    def __init__(
            self,
            robot: IterativeRobotBase,
            name: str = None,
            speed: float = 0.0,
            timeout: int = 15,
    ):
        """Constructor"""
        super().__init__()
        self.setName(name)
        self._robot = robot
        self._climb_speed: float = speed
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.climbing.move_winch(self._climb_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return self._robot.climbing.is_retracted()

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.climbing.move_winch(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.climbing}


class ClimberDrive(Command):

    def __init__(self,
                 climber: Climber,
                 oi: OI):
        """Constructor"""
        super().__init__()
        self._climber = climber
        self._oi = oi
        now = datetime.now().strftime("%H:%M:%S:%f")
        self.setName(f"ClimberDoNothing-{now}")

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        speed = self._oi.scoring_controller.getLeftY()
        if abs(speed) < 0.2:
            speed = 0.0
        self._climber.move_winch(speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, interrupted: bool):
        """Called once after isFinished returns true"""
        self._climber.move_winch(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end(interrupted=True)

    def getRequirements(self) -> set[Subsystem]:
        return {self._climber}


class DoNothingClimber(Command):

    def __init__(
            self,
            climber: Climber,
            oi: OI,
    ):
        """Constructor"""
        super().__init__()
        self._climber = climber
        self._oi = oi
        now = datetime.now().strftime("%H:%M:%S:%f")
        self.setName(f"ClimberDoNothing-{now}")

    def initialize(self):
        """Called before the Command is run for the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._climber.move_winch(0.0)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, interrupted: bool):
        """Called once after isFinished returns true"""
        self._climber.move_winch(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end(interrupted=True)

    def getRequirements(self) -> set[Subsystem]:
        return {self._climber}
