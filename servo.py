from adafruit_servokit import ServoKit


class Servo:
    def __init__(self, max_angle=120):
        self.servokit = ServoKit(channels=16)
        self.max_angle = max_angle
        for i in range(2):
            #pass
            #self.servokit.servo[i].set_pulse_width_range(1000, 2000)
            self.servokit.servo[i].actuation_range = self.max_angle

    def angle(self, index:int, angle:int)-> None:
        """
        Args:
        """
        assert 0 <= index and index <= 1
        #assert 0 <= angle and angle <= self.max_angle
        self.servokit.servo[index].angle = angle


if __name__ == '__main__':
    import time
    s = Servo(120)
    while True:
        s.angle(0, 0)
        for i in range(120):
            s.angle(0, i)
            time.sleep(0.05)
            #if i == 4:
            #    time.sleep(1)
            #else:
            #    time.sleep(0.2)
