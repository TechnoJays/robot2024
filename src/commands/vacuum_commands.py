from commands2 import Command
from commands2 import Subsystem

from oi import OI
from subsystems.vacuum import Vacuum


class Vac(Command):

    def __init__(
            self,
            vacuum: Vacuum,
            oi: OI,
            speed: float
    ):
        super().__init__()
        self._vacuum = vacuum
        self._oi = oi
        self._speed = speed

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._vacuum.move(self._speed)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, interrupted: bool):
        """Called once after isFinished returns true"""
        self._vacuum.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end(interrupted=True)

    def getRequirements(self) -> set[Subsystem]:
        return {self._vacuum}


class VacuumDrive(Command):

    def __init__(
            self,
            vacuum: Vacuum,
            oi: OI,
            scaling: float
    ):
        super().__init__()
        self._vacuum = vacuum
        self._oi = oi
        self._scaling = scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        speed = self._oi.scoring_controller.getRightTriggerAxis()
        if (abs(speed) < 0.1):
            speed = 0.0
        self._vacuum.move(speed * self._scaling)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, interrupted: bool):
        """Called once after isFinished returns true"""
        self._vacuum.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end(interrupted=True)

    def getRequirements(self) -> set[Subsystem]:
        return {self._vacuum}


class DoNothingVacuum(Command):
    def __init__(
            self,
            vacuum: Vacuum,
            oi: OI
    ):
        super().__init__()
        self._vacuum = vacuum
        self._oi = oi

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._vacuum.move(0.0)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, interrupted: bool):
        self._vacuum.move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end(interrupted=True)

    def getRequirements(self) -> set[Subsystem]:
        return {self._vacuum}
