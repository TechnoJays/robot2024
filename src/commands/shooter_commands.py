import typing

from commands2 import Command, Subsystem

from oi import OI
from subsystems.shooter import Shooter


class Shoot(Command):

    def __init__(
            self,
            shooter: Shooter,
    ):
        super().__init__()
        self._shooter = shooter

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        pass

    def execute(self) -> None:
        """
        Called repeatedly when this Command is scheduled to run
        """
        self._shooter.move(self._speed)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        if self.isTimedOut():
            return True

        return False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._shooter}


class ShooterDrive(Command):

    def __init__(
            self,
            shooter: Shooter,
            oi: OI
    ):
        super().__init__()
        self._shooter = shooter

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._shooter.move(shooter * self._stick_scaling)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return True

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._shooter}


class LowerShooter(Command):

    def __init__(
            self,
            shooter: Shooter,
    ):
        super().__init__()
        self._shooter = shooter

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._shooter.upheave(False)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._shooter}


class DoNothingShooter(Command):

    def __init__(
            self,
            shooter: Shooter
    ):
        super().__init__()
        self._shooter = shooter

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._shooter.move(0.0)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._shooter}


class RaiseShooter(Command):

    def __init__(
            self,
            shooter: Shooter
    ):
        super().__init__()
        self._shooter = shooter
        self.addRequirements(shooter)

    def initialize(self):
        """Called before the Command is run for the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._shooter.upheave(True)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._shooter}
