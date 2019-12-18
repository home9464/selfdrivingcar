import RPi.GPIO as GPIO

class Wheel:
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)  # Set Pi to use pin number when referencing GPIO pins.
        GPIO.setup(12, GPIO.OUT)  # Set GPIO pin 12 (PWM0) to output mode.
        GPIO.setup(13, GPIO.OUT)  # Set GPIO pin 13 (PWM1) to output mode.
        # PWM0 - Forward 
        GPIO.setup(10, GPIO.OUT)
        # PWM0 - Backward
        GPIO.setup(8, GPIO.OUT)
        # PWM1 - Forward
        GPIO.setup(11, GPIO.OUT)
        # PWM1 - Backward
        GPIO.setup(15, GPIO.OUT)
        self.pwm1 = GPIO.PWM(12, 100)   # Initialize PWM on pwmPin 100Hz frequency
        self.pwm2 = GPIO.PWM(13, 100)   # Initialize PWM on pwmPin 100Hz frequency
        self.pwm1.start(0) # Start PWM with 0% duty cycle
        self.pwm2.start(0) # Start PWM with 0% duty cycle
        self.pwm1_forward_flag = 0
        self.pwm2_forward_flag = 0


    def stop(self):
        self.throttle(0)

    def forward(self):
        self.throttle(100)
        GPIO.output(8, 1)
        GPIO.output(10, 0)
        GPIO.output(11, 1)
        GPIO.output(15, 0)

    def backward(self):
        self.throttle(100)
        GPIO.output(8, 0)
        GPIO.output(10, 1)
        GPIO.output(11, 0)
        GPIO.output(15, 1)

    def left(self):
        self.throttle(100)
        GPIO.output(8, 1)
        GPIO.output(10, 0)
        GPIO.output(11, 0)
        GPIO.output(15, 1)

    def right(self):
        self.throttle(100)
        GPIO.output(8, 0)
        GPIO.output(10, 1)
        GPIO.output(11, 1)
        GPIO.output(15, 0)

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
