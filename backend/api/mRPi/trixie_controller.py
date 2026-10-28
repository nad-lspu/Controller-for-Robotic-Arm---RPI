from ..rpi_gpio_module import set_servo_angle, load_model
from ultralytics import YOLO
import time
from typing import Literal

class Joint():
    def __init__(self, servo_channel=None):
        self._servo_channel = servo_channel

    @property
    def servo_channel(self):
        return self._servo_channel

    def set_angle(self, angle: int):
        if angle > 180 or angle < 0:
            raise ValueError('Servo Angle should be between 0 and 180')
        set_servo_angle(angle, self.servo_channel)

class Camera():
    def initialize():
        print('Camera has been Initialized')
    
    def close():
        print('Camera has been Closed.')

class RoboticArm():
    def __init__(self):
        self.base = Joint(servo_channel=0)
        self.lower_arm = Joint(servo_channel=1)
        self.upper_arm = Joint(servo_channel=2)
        self.fore_arm = Joint(servo_channel=3)
        self.claw = Joint(servo_channel=4)
        self.camera = Camera()
        self.model: YOLO = None

    def load_model(self):
        self.model = load_model('models/best.pt')

class UserInterface():
    def __init__(self):
        pass

    def print(string: str):
        # Show print
        pass

    def imshow(img):
        # Show image
        pass

def delay(delay: int, units: Literal['milliseconds', 'seconds'] = 'milliseconds'):
    if units == 'milliseconds':
        time.sleep(delay / 1000)
    elif units == 'seconds':
        time.sleep(delay)
    else:
        raise ValueError('Units should be "milliseconds" or "seconds"')