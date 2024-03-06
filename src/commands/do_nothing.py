from typing import Set

from commands2 import Command, Subsystem


class DoNothing(Command):
    def __init__(
            self,
            subsystem: Subsystem,
    ):
        """Constructor"""
        super().__init__()
        self._subsystem = subsystem

    def initialize(self):
        """Called before the Command is run for the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass

    def isFinished(self) -> bool:
        return True

    def getRequirements(self) -> Set[Subsystem]:
        return {self._subsystem}
