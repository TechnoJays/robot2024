# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import typing

from commands2 import Command, Subsystem

from oi import OI
from subsystems.drivetrain import Drivetrain


class TankDrive(Command):

    def __init__(
            self,
            oi: OI,
            drivetrain: Drivetrain,
    ):
        """
        Constructor

        Sets the scaling factor (`_dpad_scaling`) for "fine" control over the tank drive from the directional pad
        Sets the scaling factor (`_stick_scaling`) for general control of the tank drive from the joysticks

        Set up for "Slew Rate Limiting" based on button modifier input. If the "Slew Rate" button is compressed,
        then the robot tank drive will not use the direct input from the joystick. Instead, it will apply a
        maximum rate of change to the joystick input.

        Caveat: The way the slew rate is applied, it will also affect deceleration of the robot. That means that
        if the slew rate modifier button is depressed, that the robot will not immediately come to a stop when
        the joystick is released, it will slowly decelerate (fast deceleration is one of the primary reasons for
        robot tipping)
        """
        super().__init__()
        self._oi = oi
        self._drivetrain = drivetrain
        self._dpad_scaling = drivetrain.dpad_scaling
        self._stick_scaling = drivetrain.modifier_scaling

    def initialize(self):
        """Called before the Command is run for the first time."""
        pass

    def execute(self):
        """Called repeatedly when this Command is scheduled to run"""

        modifier = self._drivetrain.default_scaling

        if self.drivetrain.slow():
            modifier = self._drivetrain.modifier_scaling
        elif self.drivetrain.turbo():
            modifier = 1.0

        left_track: float = self.oi.driver_controller.getLeftY()
        right_track: float = self.oi.driver_controller.getRightY()
        self.drivetrain.tank_drive(left_track * modifier, right_track * modifier)

    def isFinished(self) -> bool:
        """
        If TankDrive is a registered command for the robot, it should be utilized
        as the default command for the drivetrain. As the default command for the drivetrain
        it is never finished, so we return False
        """
        return False

    def end(self, interrupted: bool) -> None:
        """
        This command expects to never be ended, and so does nothing when end is called
        """
        pass

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._drivetrain}

    @property
    def drivetrain(self) -> Drivetrain:
        return self._drivetrain

    @property
    def dpad_scaling(self) -> float:
        return self._dpad_scaling

    @property
    def stick_scaling(self):
        return self._stick_scaling

    @property
    def oi(self) -> OI:
        return self._oi


class GoTurbo(Command):

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self._drivetrain = drivetrain
        self._turbo_updated = False

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self._turbo_updated = self._drivetrain.set_turbo()

    def isFinished(self) -> bool:
        return self._turbo_updated

    def end(self, interrupted: bool) -> None:
        """
        This command is meant to be behind a button press (on press), and so should not be interruptable
        """
        pass

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._drivetrain}

    def turboUpdated(self) -> bool:
        return self._turbo_updated


class ReleaseTurbo(Command):

    def __init__(self, drivetrain: Drivetrain):
        super().__init__()
        self._drivetrain = drivetrain
        self._turbo_updated = False

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        """
        Expect release turbo to return the drivetrains turbo value, which should be false
        after being released
        """
        self._turbo_updated = not self._drivetrain.release_turbo()

    def isFinished(self) -> bool:
        return self._turbo_updated

    def end(self, interrupted: bool) -> None:
        pass

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._drivetrain}

    def turboUpdated(self) -> bool:
        return self._turbo_updated
