import RPi.GPIO as GPIO

BCM_PIN = {
    'motor1_pwm': 18, 
    'motor1_A': 15, 
    'motor1_B': 14,
    'motor2_pwm': 27, 
    'motor2_A': 17, 
    'motor2_B': 22
}

BOARD_PIN = {
    'motor1_pwm': 12, 
    'motor1_A': 10, 
    'motor1_B': 8,
    'motor2_pwm': 13, 
    'motor2_A': 11, 
    'motor2_B': 15
}

class Wheel:
    def __init__(self):
        #GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.
        GPIO.setmode(GPIO.BCM)  # Set Pi to use pin number when referencing GPIO pins.
        self.PIN = BCM_PIN
        GPIO.setup(self.PIN['motor1_pwm'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_pwm'], GPIO.OUT)
        GPIO.setup(self.PIN['motor1_A'], GPIO.OUT)
        GPIO.setup(self.PIN['motor1_B'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_A'], GPIO.OUT)
        GPIO.setup(self.PIN['motor2_B'], GPIO.OUT)
        # the 1st motor
        self.pwm1 = GPIO.PWM(self.PIN['motor1_pwm'], 1000)   # Initialize PWM on pwmPin 1000Hz frequency
        # the 2nd motor
        self.pwm2 = GPIO.PWM(self.PIN['motor2_pwm'], 1000)   # Initialize PWM on pwmPin 1000Hz frequency
        self.pwm1.start(0) # Start the 1st motor  with 0% duty cycle
        self.pwm2.start(0) # Start the 2nd motor  with 0% duty cycle
        self.pwm1_forward_flag = 0
        self.pwm2_forward_flag = 0

    def stop(self):
        self.throttle(0)

    def _pin(self, a, b, c, d):
        GPIO.output(self.PIN['motor1_A'], a)
        GPIO.output(self.PIN['motor1_B'], b)
        GPIO.output(self.PIN['motor2_A'], c)
        GPIO.output(self.PIN['motor2_B'], d)

    def forward(self):
        self.throttle(100)
        self._pin(0, 1, 1, 0)

    def backward(self):
        self.throttle(100)
        self._pin(1, 0, 0, 1)

    def left(self):
        self.throttle(100)
        self._pin(0, 1, 0, 1)

    def right(self):
        self.throttle(100)
        self._pin(1, 0, 1, 0)

    def drive(self, direction:int) -> None:
        assert 0 <= direction and direction <= 4
        if direction == 0:
            self.stop()
        elif direction == 1:
            self.forward()
        elif direction == 2:
            self.backward()
        elif direction == 3:
            self.left()
        elif direction == 4:
            self.right()
            
    def throttle(self, percentage: int = 50) -> None:
        assert 0 <= percentage and percentage <= 100
        self.pwm1.ChangeDutyCycle(percentage)
        self.pwm2.ChangeDutyCycle(percentage)

    def close(self):
        self.pwm1.stop()
        self.pwm2.stop()
        GPIO.cleanup()

if __name__ =='__main__':
    drive = Wheel()
    for _ in range(10):
        drive.drive(0)