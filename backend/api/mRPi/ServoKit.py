class Servo:
        def __init__(self):
            self.angle = 0

        def set_pulse_width_range(self, min_width: int, max_width: int):
            self.min_width = min_width
            self.max_width = max_width

class ServoKit:
    def __init__(self, channels: int):
        self.channels = channels

        self.servo: list[Servo] = []

        for r in range(self.channels):
            new_servo = Servo()
            self.servo.append(new_servo)