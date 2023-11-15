from commands2 import CommandBase

from subsystems.shooter import Shooter


class LowerFlipper(CommandBase):

    def __init__(
            self,
            shooter: Shooter
    ):
        super().__init__()
        self._shooter = shooter
        self.addRequirements(shooter)

    def initialize(self):
        """Called before the Command is run for the first time."""
        self._shooter.upheave(False)

    def isFinished(self):
        """
        Always returns true, as the command is executed on initialization, and does not
        need to repeat
        """
        return True
