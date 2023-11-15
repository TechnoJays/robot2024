from commands2 import CommandBase, SubsystemBase


class DoNothing(CommandBase):
    def __init__(
            self,
            subsystem: SubsystemBase,
    ):
        """Constructor"""
        super().__init__()
        self.addRequirements(subsystem)

    def initialize(self):
        """Called before the Command is run for the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        pass

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        pass
