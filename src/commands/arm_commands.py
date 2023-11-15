# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import typing

from commands2 import CommandBase, Subsystem

from subsystems.arm import Arm


class Raise(CommandBase):
    """
    Command to trigger the Arm subsystem to raise

    There must be a way to limit how far the arm will raise (digital limit switch)
    """

    def __init__(self,
                 arm: Arm,
                 joy_button: typing.Callable[[], bool]
                 ) -> None:
        """
        Set up the raise command with the arm subsystem and joystick button it needs
        """
        super().__init__()
        self._arm = arm
        self._joyInput = joy_button
        self.addRequirements(arm)

    def initialize(self) -> None:
        """
        Initialization of the Arm raise command subsystem

        Should initialize the measurement of the Arms position to "0" or the starting position
        """
        self._arm.move(0.0)
        pass

    def end(self, interrupted: bool) -> None:
        self._arm.move(0.0)

    def execute(self) -> None:
        """
        The steps to execute everytime this command is called
        """
        self._arm.move(1.0)

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._arm}

    def isFinished(self) -> bool:
        """
        Determines if the Arm should continue to raise based on whether the joystick button is
        still pressed
        """
        return self._joyInput()

    @property
    def arm(self):
        return self._arm


class ArmMove(CommandBase):
    """
    Command to trigger the Arm subsystem to raise

    There must be a way to limit how far the arm will and lower
    """

    def __init__(self,
                 arm: Arm,
                 joy_stick: typing.Callable[[], float]
                 ) -> None:
        """
        Set up the move command with the joystick "stick" axis and Arm subsystem
        """
        super().__init__()
        self._arm = arm
        # python lambda returning reading of a joystick axis
        self._joyInput = joy_stick
        self.addRequirements(arm)

    def initialize(self) -> None:
        """
        Initialization of the Arm raise command subsystem

        Should initialize the measurement of the Arms position to "0" or the starting position
        """
        self._arm.move(0.0)

    def end(self, interrupted: bool) -> None:
        self._arm.move(0.0)

    def execute(self) -> None:
        """
        The steps to execute everytime this command is called
        """
        self._arm.move(self._joyInput())

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._arm}

    def isFinished(self) -> bool:
        """
        Determines whether the Arm movement command is finished ... never

        This command expects to be run indefinitely, and assumes it is never done until it
        is interrupted
        """
        return False


class Lower(CommandBase):
    """
    Command to trigger the Arm subsystem to lower

    There must be a way to limit how far the arm will lower
    """

    def __init__(self,
                 arm: Arm,
                 joy_button: typing.Callable[[], bool]
                 ) -> None:
        """
        Set up the lower command with the Arm subsystem and joystick button that triggers it
        """
        super().__init__()
        self._arm = arm
        self._joyInput = joy_button
        self.addRequirements(arm)

    def initialize(self) -> None:
        """
        Initialization of the Arm raise command subsystem

        Should initialize the measurement of the Arms position to "0" or the starting position
        """
        pass

    def end(self, interrupted: bool) -> None:
        self._arm.move(0.0)

    def execute(self) -> None:
        """
        The steps to execute everytime this command is called
        """
        self._arm.move(-1.0)

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._arm}


class DoNothingArm(CommandBase):
    """
    The suggested default command for the Arm

    Sets the speed of the arm to zero, which should immediately stop its movement, regardless of previous
    commands running for the arm
    """

    def __init__(
            self,
            arm: Arm
    ):
        super().__init__()
        self._arm = arm
        self.addRequirements(arm)

    def initialize(self) -> None:
        """Called before the Command is run for the first time."""
        self._arm.move(0.0)

    def end(self, interrupted: bool) -> None:
        self._arm.move(0.0)
        """Called once after isFinished returns true"""

    def execute(self) -> None:
        """Called repeatedly when this Command is scheduled to run"""
        self._arm.move(0.0)

    def isFinished(self) -> bool:
        """Returns true when the Command no longer needs to be run"""
        return False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._arm}

    @property
    def arm(self) -> Arm:
        return self._arm
