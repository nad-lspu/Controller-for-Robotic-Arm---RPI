import platform
from ultralytics import YOLO

"""
Checks if operating system is in Windows.
Allows mock development in windows without errors
even if the code is not run on Raspberry Pi.

When running on Raspberry Pi:
=>  pip install -r rpi-requirements.txt
"""
if platform.system() == 'Windows' or platform.system() == 'Darwin':
    from .mRPi import GPIO
    from .mRPi.ServoKit import ServoKit
else: 
    import RPi.GPIO as GPIO # type: ignore
    from adafruit_servokit import ServoKit # type: ignore

POWER_BUTTON_PIN = 17
SERVO_CHANNELS = 16

kit = ServoKit(channels=SERVO_CHANNELS)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(POWER_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def set_servo_angle(angle: int, servo_channel: int):
    kit.servo[servo_channel].angle = (
        angle 
        if servo_channel == 1 
        else 160 
        if servo_channel == 4 and angle > 160 
        else 180 - angle
    )
    print(f'Servo Channel {servo_channel} to angle {angle}')

def setup_shutdown_detection():

    def shutdown_device():
        GPIO.cleanup()
        for i in range(SERVO_CHANNELS):
            set_servo_angle(90, i)

    # GPIO.add_event_detect(POWER_BUTTON_PIN, GPIO.FALLING, callback=shutdown_device, bouncetime=200)

def load_model(modelPath: str) -> YOLO:
    return YOLO(modelPath)

def gpio_cleanup():
    GPIO.cleanup()

for i in range(SERVO_CHANNELS):
    default_angle_mapping = {
        0: 90, 1: 25, 2: 0, 3: 80, 4: 90, 5: 90, 6: 90, 7: 90,
        8: 90, 9: 90, 10: 90, 11: 90, 12: 90, 13: 90, 14: 90, 15: 90,
    }

    if (len(default_angle_mapping) != SERVO_CHANNELS):
        raise ValueError('Variable default_angle_mapping length should be equal to the servo channels specified.')

    set_servo_angle(default_angle_mapping[i], i)
    kit.servo[i].set_pulse_width_range(500, 2550)