# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser
from typing import Optional

from commands2 import SubsystemBase
from wpilib import ADXRS450_Gyro
from wpilib import PWMMotorController, PWMVictorSPX
from wpilib import SmartDashboard
from wpilib.drive import DifferentialDrive
from wpimath.filter import SlewRateLimiter


class Drivetrain(SubsystemBase):
    # Config file section names
    GENERAL_SECTION = "DrivetrainGeneral"
    LEFT_MOTOR_SECTION = "DrivetrainLeftMotor"
    RIGHT_MOTOR_SECTION = "DrivetrainRightMotor"
    GYRO_SECTION = "DrivetrainGyro"

    # Key names within each section (many of the keys are used across sections)
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    # ARCADE_DRIVE_ROTATION_INVERTED_KEY = "ARCADE_DRIVE_ROTATION_INVERTED"
    TYPE_KEY = "TYPE"
    CHANNEL_KEY = "CHANNEL"
    REVERSED_KEY = "REVERSED"
    MAX_SPEED_KEY = "MAX_SPEED"
    DEFAULT_SCALING_KEY = "DEFAULT_SCALING"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"
    DPAD_SCALING_KEY = "DPAD_SCALING"

    # Default arcade drive rotation modifier to -1 for DifferentialDrive
    _arcade_rotation_modifier: float = -1

    def __init__(
            self,
            config: ConfigParser,
    ):
        self._config = config
        self._init_components()
        self._gyro: Optional[ADXRS450_Gyro] = None
        self._gyro_angle: float = 0.0
        Drivetrain._update_smartdashboard_tank_drive(0.0, 0.0)
        Drivetrain._update_smartdashboard_arcade_drive(0.0, 0.0)
        super().__init__()

    def _init_components(self):
        self._max_speed = self._config.getfloat(
            Drivetrain.GENERAL_SECTION, Drivetrain.MAX_SPEED_KEY
        )
        self._modifier_scaling = self._config.getfloat(
            Drivetrain.GENERAL_SECTION, Drivetrain.MODIFIER_SCALING_KEY
        )
        self._dpad_scaling = self._config.getfloat(
            Drivetrain.GENERAL_SECTION, Drivetrain.DPAD_SCALING_KEY
        )
        self._default_scaling = self._config.getfloat(
            Drivetrain.GENERAL_SECTION, Drivetrain.DEFAULT_SCALING_KEY
        )

        self._left_motor = self._init_motor(Drivetrain.LEFT_MOTOR_SECTION)
        self._right_motor = self._init_motor(Drivetrain.RIGHT_MOTOR_SECTION)

        if self._left_motor and self._right_motor:
            self._robot_drive = DifferentialDrive(self._left_motor, self._right_motor)
            self._robot_drive.setSafetyEnabled(False)

        self._l_slew_rate_limiter = SlewRateLimiter(0.5)
        self._r_slew_rate_limiter = SlewRateLimiter(0.5)

    def _init_motor(self, config_section: str) -> PWMVictorSPX:
        motor = PWMVictorSPX(self._config.getint(config_section, Drivetrain.CHANNEL_KEY))
        motor.setInverted(self._config.getboolean(config_section, Drivetrain.INVERTED_KEY))
        if not self._config.getboolean(config_section, Drivetrain.ENABLED_KEY):
            motor.disable()
        return motor

    def reset_gyro_angle(self) -> float:
        if self._gyro:
            self._gyro.reset()
            self._gyro_angle = self._gyro.getAngle()
        self._update_smartdashboard_sensors(self._gyro_angle)
        return self._gyro_angle

    def is_gyro_enabled(self) -> bool:
        return self._gyro is not None

    @property
    def arcade_rotation_modifier(self) -> float:
        return self._arcade_rotation_modifier

    def tank_drive(self, left_speed: float, right_speed: float):
        # TODO: Insert slew rate filters
        left = left_speed * self._max_speed
        right = right_speed * self._max_speed
        self._robot_drive.tankDrive(right, left, False)
        Drivetrain._update_smartdashboard_tank_drive(left_speed, right_speed)
        self.get_gyro_angle()
        self._update_smartdashboard_sensors(self._gyro_angle)

    def arcade_drive(
            self,
            linear_distance: float,
            turn_angle: float,
            squared_inputs: bool = True
    ):
        determined_turn_angle = self._modify_turn_angle(turn_angle)
        if self._robot_drive:
            self._robot_drive.arcadeDrive(
                linear_distance, determined_turn_angle, squared_inputs
            )
        Drivetrain._update_smartdashboard_arcade_drive(
            linear_distance, determined_turn_angle
        )
        self.get_gyro_angle()
        self._update_smartdashboard_sensors(self._gyro_angle)

    def _modify_turn_angle(self, turn_angle: float) -> float:
        """
        Method to support switch from pyfrc RobotDrive to pyfrc DifferentialDrive see:
        https://robotpy.readthedocs.io/projects/wpilib/en/latest/wpilib.drive/DifferentialDrive.html#wpilib.drive.differentialdrive.DifferentialDrive
        """
        return self._arcade_rotation_modifier * turn_angle

    @staticmethod
    def _update_smartdashboard_tank_drive(left: float, right: float):
        SmartDashboard.putNumber("Drivetrain Left Speed", left)
        SmartDashboard.putNumber("Drivetrain Right Speed", right)

    @staticmethod
    def _update_smartdashboard_arcade_drive(linear: float, turn: float):
        SmartDashboard.putNumber("Drivetrain Linear Speed", linear)
        SmartDashboard.putNumber("Drivetrain Turn Speed", turn)

    @staticmethod
    def _update_smartdashboard_sensors(gyro_angle: float):
        SmartDashboard.putNumber("Gyro Angle", gyro_angle)

    @property
    def left_motor(self) -> PWMMotorController:
        return self._left_motor

    @property
    def right_motor(self) -> PWMMotorController:
        return self._right_motor

    @property
    def robot_drive(self) -> DifferentialDrive:
        return self._robot_drive

    @property
    def max_speed(self) -> float:
        return self._max_speed

    @property
    def modifier_scaling(self) -> float:
        return self._modifier_scaling

    @property
    def dpad_scaling(self) -> float:
        return self._dpad_scaling
    
    @property
    def default_scaling(self) -> float:
        return self._default_scaling

    def get_gyro_angle(self) -> float:
        if self._gyro:
            self._gyro_angle = self._gyro.getAngle()
        return self._gyro_angle

    @property
    def gyro(self):
        return self._gyro

    @property
    def left_slew_rate(self):
        return self._l_slew_rate_limiter

    @property
    def right_slew_rate(self):
        return self._r_slew_rate_limiter
