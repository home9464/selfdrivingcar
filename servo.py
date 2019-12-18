from adafruit_servokit import ServoKit


class Servo:
    def __init__(self):
        self.servokit = ServoKit(channels=16)
        self.max_angle = 120
        for i in range(2):
            self.servokit.servo[i].set_pulse_width_range(1000, 2000)
            self.servokit.servo[i].actuation_range = self.max_angle

    def angle(self, index:int, angle:int)-> None:
        """
        Args:
        """
        assert 0 <= index and index <= 1
        assert 0 <= angle and angle <= self.max_angle
        self.servokit.servo[index].angle = angle


