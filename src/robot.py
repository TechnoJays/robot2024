import logging

import wpilib
from commands2 import CommandScheduler, SequentialCommandGroup
from commands2 import TimedCommandRobot

from autonomous.autonomous_drive_commands import MoveFromLine
from robot_controller import RobotController

logging.basicConfig(level=logging.INFO)


class RetrojaysRobot(TimedCommandRobot):
    SIM_SUBSYSTEMS_CONFIG_PATH = "configs/subsystems.ini"
    SIM_JOYSTICK_CONFIG_PATH = "configs/joysticks.ini"
    SIM_AUTONOMOUS_CONFIG_PATH = "configs/autonomous.ini"
    _robot_controller: RobotController = None
    _autonomous_command_group: SequentialCommandGroup = None

    def autonomousInit(self):
        # Schedule the autonomous command
        # TODO move into robot controller for better mgmt?
        # self._autonomous_command_group = self._robot_controller.get_auto_chooser().getSelected()
        self._autonomous_command_group = MoveFromLine(self._robot_controller.drivetrain,
                                                      self._robot_controller.autonomous_config)
        logging.info(f"Chosen Auto Mode: {self._autonomous_command_group}")
        if self._autonomous_command_group:
            self._autonomous_command_group.schedule()

    def autonomousPeriodic(self):
        """
        This function is called periodically during autonomous.
        The scheduler is what runs the periodioc processes for managing
        commands during autonomous
        """
        pass

    def disabledInit(self):
        logging.debug("Robot Code Disabled Initialized")
        pass

    def disabledPeriodic(self):
        # logging.debug("Robot Code in disabled periodic loop")
        pass

    def disabledExit(self):
        logging.debug("Robot Code Disabled Exit")
        pass

    def robotInit(self):
        """
        This function is called upon robot startup and creates the main "Robot Controller" which contains
        the majority of the robot code

        This function also checks if the robot is currently running as a simulation
        """
        if self.isSimulation():
            logging.info("### RUNNING AS SIMULATION ###")
            self._robot_controller = RobotController(self.SIM_SUBSYSTEMS_CONFIG_PATH,
                                                     self.SIM_JOYSTICK_CONFIG_PATH,
                                                     self.SIM_AUTONOMOUS_CONFIG_PATH)
        else:
            self._robot_controller = RobotController()
        self._robot_controller.mappings()

    def robotPeriodic(self) -> None:
        """
        Ensures commands are run
        """
        self._robot_controller.update_sensors()
        CommandScheduler.getInstance().run()

    def teleopInit(self):
        logging.debug("Robot Code Teleop Initialized")
        if self._autonomous_command_group:
            self._autonomous_command_group.cancel()
            logging.info("Cancelled Autonomous Command in Teleop")

    def teleopPeriodic(self):
        """
        This function is called periodically during operator control.
        The scheduler is what runs the periodic processes for managing
        commands during autonomous
        """
        pass

    def testInit(self):
        pass

    def testPeriodic(self):
        """
        This function is called periodically during test mode.
        """
        pass

    @property
    def controller(self) -> RobotController:
        """ Returns the robot controller managing all robot subsystems and operator interface"""
        return self._robot_controller


if __name__ == "__main__":
    wpilib.run(RetrojaysRobot)
