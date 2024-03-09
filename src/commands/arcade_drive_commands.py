import math

from commands2 import Command, Subsystem

from subsystems.drivetrain import Drivetrain
from util.stopwatch import Stopwatch


class DriveTime(Command):

    def __init__(
            self,
            drivetrain: Drivetrain,
            duration: float,
            speed: float,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed
        self.addRequirements(drivetrain)

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        self._stopwatch.start()

    def execute(self) -> None:
        """Called repeatedly when this Command is scheduled to run"""
        self.drivetrain.arcade_drive(self._speed, 0.0, False)
        return Command.execute(self)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        return self._stopwatch.elapsed_time_in_secs() >= self._duration

    def end(self, interrupted: bool) -> None:
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self._drivetrain.arcade_drive(0.0, 0.0)

    def interrupted(self) -> None:
        """
        Called when another command which requires one or more of the same subsystems is scheduled to run

        This method is removed and  no longer needs to be overriden
        """
        self.end(True)

    def getRequirements(self) -> set[Subsystem]:
        return {self._drivetrain}

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def duration(self) -> float:
        return self._duration

    @property
    def stopwatch(self) -> Stopwatch:
        return self._stopwatch

    @property
    def speed(self) -> float:
        return self._speed


class TurnDegrees(Command):

    def __init__(
            self,
            drivetrain: Drivetrain,
            degrees_change: float,
            speed: float,
            threshold: float,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._degrees_change = degrees_change
        self._speed = speed
        self._degree_threshold = threshold
        self._target_degrees = 0.0
        self.addRequirements(drivetrain)

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        self._target_degrees = (self._drivetrain.get_gyro_angle() + self._degrees_change)

    def execute(self) -> None:
        """
        Called repeatedly when this Command is scheduled to run
        """
        degrees_left = self._target_degrees - self._drivetrain.get_gyro_angle()
        turn_speed = self._speed * TurnDegrees._determine_direction(degrees_left)
        self._drivetrain.arcade_drive(0.0, turn_speed, False)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        current = self._drivetrain.get_gyro_angle()
        # If abs(target - current) < threshold then return true
        return (
                math.fabs(self._target_degrees - current) <= self._degree_threshold
        )

    def end(self, interrupted: bool) -> None:
        """Called once after isFinished returns true"""
        self._drivetrain.arcade_drive(0.0, 0.0)

    @staticmethod
    def _determine_direction(degrees_left: float) -> float:
        """Based on the degrees left, determines the direction of the degrees to turn"""
        return 1.0 if degrees_left >= 0 else -1.0

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def degrees_change(self) -> float:
        return self._degrees_change

    @property
    def degree_threshold(self) -> float:
        return self._degree_threshold

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def target_degrees(self) -> float:
        return self._target_degrees


class TurnDegreesAbsolute(Command):

    def __init__(
            self,
            drivetrain: Drivetrain,
            degrees_target: float,
            speed: float,
            threshold: float,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._target_degrees = degrees_target
        self._speed = speed
        self._degree_threshold = threshold
        self.addRequirements(drivetrain)

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        return Command.initialize(self)

    def execute(self) -> None:
        """Called repeatedly when this Command is scheduled to run"""
        degrees_left = self._target_degrees - self._drivetrain.get_gyro_angle()
        turn_speed = self._speed * TurnDegreesAbsolute._determine_direction(
            degrees_left
        )
        self._drivetrain.arcade_drive(0.0, turn_speed, False)
        return Command.execute(self)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        current = self._drivetrain.get_gyro_angle()
        # If abs(target - current) < threshold then return true
        return (
                math.fabs(self._target_degrees - current) <= self._degree_threshold
        )

    def end(self, interrupted: bool) -> None:
        """Called once after isFinished returns true"""
        self._drivetrain.arcade_drive(0.0, 0.0)

    @staticmethod
    def _determine_direction(degrees_left: float) -> float:
        """Based on the degrees left, returns -1 for turn right, returns 1 for turn left"""
        return 1.0 if degrees_left >= 0 else -1.0

    def getRequirements(self) -> set[Subsystem]:
        return {self._drivetrain}

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def speed(self) -> float:
        return self._speed

    @property
    def target_degrees(self) -> float:
        return self._target_degrees

    @property
    def degree_threshold(self) -> float:
        return self._degree_threshold


class TurnTime(Command):

    def __init__(
            self,
            drivetrain: Drivetrain,
            duration: float,
            speed: float,
    ):
        """Constructor"""
        super().__init__()
        self._drivetrain = drivetrain
        self._stopwatch = Stopwatch()
        self._duration = duration
        self._speed = speed
        self.addRequirements(drivetrain)

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        self._stopwatch.start()

    def execute(self) -> None:
        """Called repeatedly when this Command is scheduled to run"""
        self._drivetrain.arcade_drive(0.0, self._speed, False)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        return (
                self._stopwatch.elapsed_time_in_secs() >= self._duration
        )

    def end(self, interrupted: bool) -> None:
        """Called once after isFinished returns true"""
        self._stopwatch.stop()
        self._drivetrain.arcade_drive(0.0, 0.0)

    @property
    def drivetrain(self):
        return self._drivetrain

    @property
    def speed(self):
        return self._speed

    @property
    def stopwatch(self):
        return self._stopwatch

    @property
    def duration(self):
        return self._duration
