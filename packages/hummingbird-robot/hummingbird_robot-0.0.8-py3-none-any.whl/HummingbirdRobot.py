import time
from BirdBrain import Hummingbird
#from pygame.locals import *

from HummingbirdDualMotorDriver import *
from HummingbirdJoystick import *
from HummingbirdJoystickCalculator import *

class HummingbirdRobot:
    def __init__(self, motor_device = 'A', joystick_device = None, minimum_motor_speed = None, joystick_calculator = None, joystick_rotation = None):
        self.motor_device = motor_device
        self.joystick_device = joystick_device
        self.minimum_motor_speed = minimum_motor_speed
        self.joystick_calculator = joystick_calculator
        self.joystick_rotation = joystick_rotation

        if self.minimum_motor_speed is None: self.minimum_motor_speed = HummingbirdDualMotorDriver.MINIMUM_SPEED
        if self.joystick_rotation is None: self.joystick_rotation = HummingbirdJoystick.DEFAULT_ROTATION

        self.motors = None
        self.joystick = None

        if self.motor_device is not None:
            try:
                self.motors = HummingbirdDualMotorDriver(self.motor_device, self.minimum_motor_speed)
            except ConnectionRefusedError:
                print("Motor device not available")
                raise

        if self.joystick_device is not None:
            try:
                self.joystick = None if self.joystick_device is None else HummingbirdJoystick(self.joystick_device, self.joystick_rotation)

                if self.joystick_calculator is None: self.joystick_calculator = HummingbirdJoystickCalculator()
            except ConnectionRefusedError:
                print("Joystick device not available")
                raise

    def move(self):
        if self.motors is not None:
            x, y = self.joystick.values()

            self.motors.move(self.joystick_calculator.speeds(x, y))
