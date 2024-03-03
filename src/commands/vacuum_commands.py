from commands2 import Command, TimedCommandRobot, Subsystem
from commands2 import Subsystem
from wpilib import IterativeRobotBase

from oi import UserController, JoystickAxis


class Vac(Command):

    def __init__(
            self,
            robot: TimedCommandRobot,
            speed: float,
            timeout: int = 15,
    ):
        super().__init__()
        self._robot = robot
        self._speed = speed
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.vacuum().move(self._speed)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self, **kwargs):
        """Called once after isFinished returns true"""
        self._robot.vacuum().move(0.0)

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.controller().vacuum()}


class VacuumDrive(Command):
    _dpad_scaling: float
    _stick_scaling: float
    _robot: IterativeRobotBase = None

    def __init__(
            self,
            robot: IterativeRobotBase,
            name: str = "VacuumDrive",
            modifier_scaling: float = 1.0,
            dpad_scaling: float = 0.4,
            timeout: int = 15,
    ):
        super().__init__()
        self.setName(name)
        self._robot = robot
        self.withTimeout(timeout)
        self._dpad_scaling = dpad_scaling
        self._stick_scaling = modifier_scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        vacuum: float = self._robot.oi.get_axis(
            UserController.SCORING, JoystickAxis.RIGHTY
        )
        self._robot.vacuum.move(vacuum * self._stick_scaling)

        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return True

    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.vacuum}


class DoNothingVacuum(Command):
    def __init__(
        self,
        robot: IterativeRobotBase,
        name: str = "DoNothingVacuum",
        timeout: int = 15,
    ):
        super().__init__()
        self.setName(name)
        self._robot = robot
        self.withTimeout(timeout)

    def initialize(self):
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""
        self._robot.vacuum.move(0.0)
        return Command.execute(self)

    def isFinished(self):
        """Returns true when the Command no longer needs to be run"""
        return False

    def end(self):
        """Called once after isFinished returns true"""
        pass

    def interrupted(self):
        """Called when another command which requires one or more of the same subsystems is scheduled to run"""
        self.end()

    def getRequirements(self) -> set[Subsystem]:
        return {self._robot.vacuum}
