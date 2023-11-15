# Copyright (c) Southfield High School Team 94
# Open Source Software; you can modify and / or share it under the terms of
# the MIT license file in the root directory of this project
from configparser import ConfigParser
from typing import Optional

from commands2 import SubsystemBase
from wpilib import PWMVictorSPX, SmartDashboard, AnalogPotentiometer, DigitalInput
from wpimath.filter import SlewRateLimiter

ARM_DASHBOARD_ADJUSTED_SPEED = "0_Arm-02-Adjusted-Speed"
ARM_DASHBOARD_LOWER_LIMIT = "0_Arm-06-Lower-Limit-Switch"
ARM_DASHBOARD_POT_READING = "0_Arm-03-Potentiometer"
ARM_DASHBOARD_SLEW_RATE = "0_Arm-04-Slew-Rate"
ARM_DASHBOARD_SPEED = "0_Arm-01-Speed"
ARM_DASHBOARD_UPPER_LIMIT = "0_Arm-05-Upper-Limit-Switch"


class Arm(SubsystemBase):
    # Config file section name
    GENERAL_SECTION = "ArmGeneral"
    POTENTIOMETER_SECTION = "ArmPotentiometer"
    LOWER_LIMIT_SWITCH_SECTION = "ArmBottomLimitSwitch"
    UPPER_LIMIT_SWITCH_SECTION = "ArmTopLimitSwitch"

    # Config keys
    CHANNEL_KEY = "CHANNEL"
    ENABLED_KEY = "ENABLED"
    INVERTED_KEY = "INVERTED"
    MAX_SPEED_KEY = "MAX_SPEED"
    MAX_STABLE_SPEED_KEY = "MAX_STABLE_SPEED"
    MODIFIER_SCALING_KEY = "MODIFIER_SCALING"
    POT_RANGE_KEY = "FULL_RANGE"
    SLEW_RATE = "SLEW_RATE"

    def __init__(
            self,
            config: ConfigParser
    ) -> None:
        self._config = config
        self._enabled = self._config.getboolean(
            Arm.GENERAL_SECTION, Arm.ENABLED_KEY
        )
        self._init_components()
        print("***Arm initialized***")
        super().__init__()

    def _init_components(self) -> None:
        self._max_stable_speed = self._config.getfloat(Arm.GENERAL_SECTION, Arm.MAX_STABLE_SPEED_KEY)
        # We have to be able to limit the max speed as some percentage of the max stable speed
        self._max_speed = self._config.getfloat(Arm.GENERAL_SECTION, Arm.MAX_SPEED_KEY)

        # initialize potentiometer for reading rotations on arm motor
        self._arm_pot_range = self._config.getfloat(Arm.POTENTIOMETER_SECTION, Arm.POT_RANGE_KEY)
        arm_pot_channel = self._config.getint(Arm.POTENTIOMETER_SECTION, Arm.CHANNEL_KEY)
        self._arm_pot = AnalogPotentiometer(arm_pot_channel, self._arm_pot_range)

        if self._enabled:
            print("*** Arm enabled ****")
            self._motor = PWMVictorSPX(
                self._config.getint(Arm.GENERAL_SECTION, Arm.CHANNEL_KEY)
            )
            self._motor.setInverted(
                self._config.getboolean(Arm.GENERAL_SECTION, Arm.INVERTED_KEY)
            )
            print("*** Arm PWM Configured ****")
        else:
            self._motor = None

        self._modifier_scaling: Optional[float] = None

        self._lower_limit_switch = self._init_limit_switch(Arm.LOWER_LIMIT_SWITCH_SECTION)
        self._lower_limit_switch_inverted = self._config.getboolean(
            Arm.LOWER_LIMIT_SWITCH_SECTION, Arm.INVERTED_KEY
        )

        self._upper_limit_switch = self._init_limit_switch(Arm.UPPER_LIMIT_SWITCH_SECTION)
        self._upper_limit_switch_inverted = self._config.getboolean(
            Arm.UPPER_LIMIT_SWITCH_SECTION, Arm.INVERTED_KEY
        )

        self._slew_rate_of_change = self._config.getfloat(
            Arm.GENERAL_SECTION, Arm.SLEW_RATE
        )
        self._slew_rate = SlewRateLimiter(self._slew_rate_of_change)

        Arm._update_smartdashboard(0.0, 0.0, self._arm_pot.get())
        self._smartdashboard_display_components()

    def _init_limit_switch(self, config_section: str) -> DigitalInput:
        """
        Initialize a limit switch based on a subsystems configuration section
        """
        channel = self._config.getint(config_section, Arm.CHANNEL_KEY)
        limit_switch = DigitalInput(channel)
        return limit_switch

    def move(self, speed: float) -> None:
        """
        Set the speed of the motor based on the speed passed into the move method
        """
        if not self._enabled:
            pass

        if speed < 0 and not self.is_fully_retracted():
            adjusted_speed = speed * self._max_speed
        elif speed > 0 and not self.is_fully_extended():
            adjusted_speed = speed * self._max_speed
        else:
            adjusted_speed = 0.0

        if self._motor:
            self._motor.set(adjusted_speed)
            # uncomment to introduce to slew rate filter
            # self._motor.set(self._slew_rate.calculate(adjusted_speed))
        Arm._update_smartdashboard(speed, adjusted_speed, self._arm_pot.get())

    # def move_angular(self, angle: float, speed: float) -> None:
    #     if not self._enabled:
    #         pass
    #     speed = speed % 1.0
    #     adjusted_speed = speed * self._max_speed
    #     if self._motor:
    #         self._motor.set(adjusted_speed)

    def is_fully_extended(self) -> bool:
        """
        Check upper limit switch to determine if the Arm has raised to its upper constraint
        """
        extended = self._limit_value(
            self._upper_limit_switch) if not self._upper_limit_switch_inverted else not self._limit_value(
            self._upper_limit_switch)
        return extended

    def is_fully_retracted(self) -> bool:
        """
        Check lower limit switch to determine if the Arm has lowered to its lower constraint
        """
        retracted = self._limit_value(
            self._lower_limit_switch) if not self._lower_limit_switch_inverted else not self._limit_value(
            self._lower_limit_switch)
        return retracted

    @staticmethod
    def _limit_value(switch: DigitalInput) -> bool:
        if switch is not None:
            return switch.get()
        else:
            return False

    @staticmethod
    def _update_smartdashboard(speed: float, adjusted_speed: float, pot_reading: float) -> None:
        SmartDashboard.putNumber(ARM_DASHBOARD_SPEED, speed)
        SmartDashboard.putNumber(ARM_DASHBOARD_ADJUSTED_SPEED, adjusted_speed)
        SmartDashboard.putNumber(ARM_DASHBOARD_POT_READING, pot_reading)

    def _smartdashboard_display_components(self) -> None:
        SmartDashboard.putNumber(ARM_DASHBOARD_SLEW_RATE, self._slew_rate_of_change)
        SmartDashboard.putBoolean(ARM_DASHBOARD_UPPER_LIMIT, self._limit_value(self._upper_limit_switch))
        SmartDashboard.putBoolean(ARM_DASHBOARD_LOWER_LIMIT, self._limit_value(self._lower_limit_switch))

    @property
    def upper_limit_switch(self) -> DigitalInput:
        return self._upper_limit_switch

    @property
    def lower_limit_switch(self) -> DigitalInput:
        return self._lower_limit_switch

    @property
    def motor(self):
        return self._motor
