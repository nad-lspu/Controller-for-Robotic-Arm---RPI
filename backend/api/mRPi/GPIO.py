# Mock Module of RPi.GPIO
## For Development in Computer without errors
from collections.abc import Callable

BCM = 'BCM'
BOARD = 'BOARD'
OUT = 'OUT'
IN = 'IN'
LOW = 0
HIGH = 1
PUD_DOWN = 0
PUD_UP = 1
FALLING = 0
RISING = 1

mode = ''
state = LOW

def setmode(mode: str):
    print(f'Pin Selectrion Mode set to {mode}')

def setwarnings(warnings: bool):
    print(f'Warnings set to {warnings}')

def setup(pin_num: int, pin_mode: str, pull_up_down = None):
    print(
        f'Pin {pin_num} set to {pin_mode} {f'in pull {'down' if not pull_up_down else 'up'} mode' if pull_up_down != None else ''}.'
    )

def input(pin_num: int):
    print(f'State of pin {pin_num} is {'LOW' if state == LOW else 'HIGH'}')
    return state

def output(pin_num: int, out_mode: str):
    global state
    state = out_mode
    print (f'Pin number {pin_num} set to {'LOW' if out_mode == LOW else 'HIGH'}')

def add_event_detect(pin_num: int, edge_event: int, callback: Callable[[], None], bouncetime: int):
    print(f'Event set on pin {pin_num} to detect {'rising' if edge_event else 'falling'} edge!')

def cleanup():
    print('GPIO pin clean up complete.')

class PWM:
    def __init__(self, pin_num: int, freq: int):
        self.pin_num = pin_num
        self.freq = freq

    def start(self, duty: int):
        print(f'PWM started at pin {self.pin_num} at {self.freq} with {duty} initial duty.')

    def stop(self):
        print('PWM stopped at pin {self.pin_num} at {self.freq}.')

    def ChangeDutyCycle(self, duty: int):
        print(f'PWM at {self.pin_num} changed duty cycle to {duty}')