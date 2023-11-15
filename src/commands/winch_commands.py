from commands2 import Command, Subsystem
from wpilib import IterativeRobotBase
from commands2 import Subsystem

from oi import UserController, JoystickAxis


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


class MoveWinch(Command):
    _robot: IterativeRobotBase = None

    def __init__(self, robot, name=None, timeout=15):
        """Constructor"""
        super().__init__()
        self.setName(name)
        self._robot = robot
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        move_speed = self._robot.oi.get_axis(UserController.SCORING, JoystickAxis.LEFTY)
        self._robot.climbing.move_winch(move_speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        self._robot.climbing.move_winch(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.climbing}
