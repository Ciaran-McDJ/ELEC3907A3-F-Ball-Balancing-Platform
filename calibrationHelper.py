# Used to help calibrate servos
# Set pin to 16, 12, or 13 for different servos and change values until 90 degrees

from gpiozero import AngularServo
from gpiozero import Servo
from time import sleep
from gpiozero.pins.pigpio import PiGPIOFactory

SERVO_1_PIN = 16


factory = PiGPIOFactory()
s1 = AngularServo(SERVO_1_PIN, pin_factory=factory, min_angle =-90, max_angle = 90, min_pulse_width = 0.00036 , max_pulse_width = 0.0023)
#s1 = Servo(SERVO_1_PIN, pin_factory=factory, min_pulse_width = 0.00051 , max_pulse_width = 0.00239)
s1.angle = 90
sleep(2)
s1.angle = 0
sleep(4)
# sleep(1)
#s1.max()
#sleep(2)
#s1.min()
#sleep(2)
s1.close()