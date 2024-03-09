# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
import configparser
import logging
from configparser import ConfigParser

from commands2 import Subsystem, SequentialCommandGroup
from wpilib import SmartDashboard, SendableChooser

from autonomous.autonomous_drive_commands import MoveFromLine
from commands.climber_commands import Climb, ClimberDrive, DoNothingClimber
from commands.do_nothing import DoNothing
from commands.shooter_commands import DoNothingShooter, RaiseShooter, LowerShooter, ShooterDrive
from commands.tank_drive_commands import TankDrive, GoTurbo, ReleaseTurbo, GoSlow, ReleaseSlow
from commands.vacuum_commands import Vac, VacuumDrive, DoNothingVacuum
from oi import OI
from subsystems.climber import Climber
from subsystems.drivetrain import Drivetrain
from subsystems.shooter import Shooter
from subsystems.vacuum import Vacuum


class RobotController:
    """
    This class is where the bulk of robot logic is declared. This is aligned to the
    `robotpy`/wpilib Command-based declarative paradigm. The majority of the structure
    of the robot outside of subsystems, and operator interface (oi) mappings are
    declared here
    """
    SUBSYSTEMS_CONFIG_PATH = "/home/lvuser/py/configs/subsystems.ini"
    JOYSTICK_CONFIG_PATH = "/home/lvuser/py/configs/joysticks.ini"
    AUTONOMOUS_CONFIG_PATH = "/home/lvuser/py/configs/autonomous.ini"

    def __init__(self,
                 subsystems_config: str = SUBSYSTEMS_CONFIG_PATH,
                 joystick_config: str = JOYSTICK_CONFIG_PATH,
                 auto_config: str = AUTONOMOUS_CONFIG_PATH
                 ) -> None:
        self._init_config(subsystems_config, joystick_config, auto_config)
        self._subsystems = self._init_subsystems()
        self._setup_autonomous_smartdashboard()

    def _init_config(self,
                     subsystems_config_path: str,
                     joystick_config_path: str,
                     autonomous_config_path: str
                     ) -> None:
        """
        Initialize config parsers for subsystems, operator interface, and autonomous
        """
        logging.debug("Reading configs")

        self._subsystems_config = configparser.ConfigParser()
        self._subsystems_config.read(subsystems_config_path)
        logging.info("Parsed subsystem configs")

        self._joystick_config = configparser.ConfigParser()
        self._joystick_config.read(joystick_config_path)
        logging.info("Parsed joystick configs")

        self._autonomous_config = configparser.ConfigParser()
        self._autonomous_config.read(autonomous_config_path)
        logging.info("Parsed autonomous configs")

    def _init_subsystems(self) -> list[Subsystem]:
        """
        Initialize subsystems managed by the robot controller
        """
        subsystems = []

        self._oi = OI(self._joystick_config)
        subsystems.append(self._oi)
        logging.info("Operator Interface Subsystem Completed Setup")

        self._drivetrain = Drivetrain(self._subsystems_config)
        subsystems.append(self._drivetrain)
        logging.info("Drivetrain Subsystem Completed Setup")

        self._vacuum = Vacuum(self._subsystems_config)
        subsystems.append(self._vacuum)
        logging.info("Feeder(Vacuum) Subsystem Completed Setup")

        self._shooter = Shooter(self._subsystems_config)
        subsystems.append(self._shooter)
        logging.info("Conveyor(Shooter) Subsystem Completed Setup")

        self._climber = Climber(self._subsystems_config)
        subsystems.append(self._climber)
        logging.info("Winch(Climber) Subsystem Completed Setup")

        # wpilib.CameraServer.launch(vision_py='vision/vision.py:start_camera')
        return subsystems

    def mappings(self) -> None:
        """
        A method to connect subsystems, the operator interface, and autonomous once
        all the subsystems have been initialized

        This method is called separately from the constructor to prevent circular dependencies
        across Subsystem and Command constructor initialization
        """

        # set up the default drive command to be tank drive
        self.drivetrain.setDefaultCommand(TankDrive(self.oi, self.drivetrain))

        # set up the default vacuum command to do nothing
        self.vacuum.setDefaultCommand(DoNothingVacuum(self.vacuum, self.oi))
        # set up the default climber command to do nothing
        self.climber.setDefaultCommand(DoNothingClimber(self.climber, self.oi))
        # set up the default shooter command to do nothing
        self.shooter.setDefaultCommand(DoNothingShooter(self.shooter))

        self.oi.driver_controller.rightBumper().onTrue(GoTurbo(self.drivetrain))
        self.oi.driver_controller.rightBumper().onFalse(ReleaseTurbo(self.drivetrain))
        self.oi.driver_controller.leftBumper().onTrue(GoSlow(self.drivetrain))
        self.oi.driver_controller.leftBumper().onFalse(ReleaseSlow(self.drivetrain))

        # set up the right bumper of the scoring controller to trigger the vacuum to spit
        self.oi.scoring_controller.rightBumper().whileTrue(Vac(self.vacuum, self.oi, 1.0))
        # set up the left bumper of the scoring controller to trigger the vacuum to suck
        self.oi.scoring_controller.leftBumper().whileTrue(Vac(self.vacuum, self.oi, -1.0))

        self.oi.scoring_controller.rightTrigger().whileTrue(VacuumDrive(self.vacuum, self.oi, 1.0))
        self.oi.scoring_controller.leftTrigger().whileTrue(VacuumDrive(self.vacuum, self.oi, -1.0))

        self.oi.scoring_controller.y().whileTrue(RaiseShooter(self.shooter, self.oi))
        self.oi.scoring_controller.a().whileTrue(LowerShooter(self.shooter, self.oi))
        self.oi.scoring_controller.rightStick().whileTrue(ShooterDrive(self.shooter, self.oi))

        self.oi.scoring_controller.leftStick().whileTrue(ClimberDrive(self.climber, self.oi))
        self.oi.scoring_controller.x().whileTrue(Climb(self.climber, self.oi, 0.5))
        self.oi.scoring_controller.b().whileTrue(Climb(self.climber, self.oi, -0.5))

    def get_auto_chooser(self) -> SendableChooser:
        return self._oi.get_auto_chooser()

    def _setup_autonomous_smartdashboard(self) -> SendableChooser:
        auto_chooser = self._oi.get_auto_chooser()
        auto_chooser.setDefaultOption("Do_Nothing", DoNothing(self._drivetrain))
        auto_chooser.addOption("Move_From_Line",
                               MoveFromLine(self._drivetrain, self._autonomous_config))
        SmartDashboard.putData(auto_chooser)
        return auto_chooser

    def update_sensors(self) -> None:
        SmartDashboard.putNumber("Climber-POT-Value-Degrees", self._climber.potentiometer().get())
        SmartDashboard.putNumber("Climber-POT-Degrees-Range", self._climber.pot_range())
        SmartDashboard.putNumber("Climber-POT-Degrees-Offset", self._climber.pot_offset())

    @property
    def drivetrain(self) -> Drivetrain:
        """
        Retrieve the "Drivetrain" subsystem managed by the robot controller
        """
        return self._drivetrain

    @property
    def shooter(self) -> Shooter:
        """
        Retrieve the "Shooter" subsystem managed by the robot controller
        """
        return self._shooter

    @property
    def oi(self) -> OI:
        """
        Retrieve the "Operator Interface" managed by the robot controller
        """
        return self._oi

    @property
    def vacuum(self) -> Vacuum:
        """
        Retrieve the "Vacuum" subsystem managed by the robot controller
        """
        return self._vacuum

    @property
    def climber(self) -> Climber:
        """
        Retrieve the "Climbing" subsystem managed by the robot controller
        """
        return self._climber

    @property
    def subsystems_config(self) -> ConfigParser:
        return self._subsystems_config

    @property
    def joystick_config(self) -> ConfigParser:
        return self._joystick_config

    @property
    def autonomous_config(self) -> ConfigParser:
        return self._autonomous_config

    @property
    def subsystems(self):
        return self._subsystems
