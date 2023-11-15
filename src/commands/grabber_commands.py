# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import typing

from commands2 import CommandBase, Subsystem

from subsystems.grabber import Grabber


class Grab(CommandBase):
    """
    Command to trigger the Grabber subsystem to pinch closed
    """

    def __init__(self, grabber: Grabber) -> None:
        """
        Constructor to connect to the Grabber subsystem and acknowledge the Grabber as a subsystem requirement
        """
        super().__init__()
        self._grabber = grabber
        self.addRequirements(grabber)

    def initialize(self) -> None:
        """
        Trigger the Grabber to close
        """
        self._grabber.grab()

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        """
        The command should immediately stop executing once the signal to close has been sent
        """
        return True

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._grabber}


class Release(CommandBase):

    def __init__(self, grabber: Grabber) -> None:
        """
        Constructor to connect to the Grabber subsystem and acknowledge the Grabber as a subsystem requirement
        """
        super().__init__()
        self._grabber = grabber
        self.addRequirements(grabber)

    def initialize(self) -> None:
        """
        Trigger the Grabber to open
        """
        self._grabber.release()

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        """
        The command should immediately stop executing once the signal to close has been sent
        """
        return True

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._grabber}


class DoNothingGrabber(CommandBase):

    def __init__(self, grabber: Grabber) -> None:
        """
        Constructor to connect to the Grabber subsystem and acknowledge the Grabber as a subsystem requirement

        Suggested default command for the grabber
        """
        super().__init__()
        self._grabber = grabber
        self.addRequirements(grabber)

    def initialize(self) -> None:
        """
        Do nothing to change the state of the grabber

        Whatever the last command setting the pneumatic solenoid received, it will continue to do
        """
        pass

    def execute(self) -> None:
        """
        Do nothing to change the state of the grabber
        """
        pass

    def isFinished(self) -> bool:
        """
        As the suggested default command for the grabber, this command is never finished until another command
        is triggered to replace it

        return False
        """
        return False

    def getRequirements(self) -> typing.Set[Subsystem]:
        return {self._grabber}
