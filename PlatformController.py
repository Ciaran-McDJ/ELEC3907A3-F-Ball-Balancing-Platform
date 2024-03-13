from gpiozero import AngularServo
from time import sleep
from calculateMotorAngle import calculateMotorAngle 
from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()
SERVO_1_PIN = 16
SERVO_3_PIN = 12
SERVO_2_PIN = 13

MAX_ANGLE = 45
MIN_ANGLE = -45

def get_servo_angles(pitch, roll, z):
    """
    returns the angles needed (servo 1, servo 2, servo 3)
    """
    angles = calculateMotorAngle(pitch, roll, z)
    print(angles)
    return angles

class PlatformController ():
    def __init__(self):
        factory = PiGPIOFactory()
        self.servo1 = AngularServo(SERVO_1_PIN, initial_angle = 0, pin_factory=factory, min_angle =-90, max_angle = 90, min_pulse_width = 0.00036 , max_pulse_width = 0.00227)
        self.servo3 = AngularServo(SERVO_3_PIN, initial_angle = 0, pin_factory=factory, min_angle =-90, max_angle = 90, min_pulse_width = 0.00050 , max_pulse_width = 0.00224)
        self.servo2 = AngularServo(SERVO_2_PIN, initial_angle = 0, pin_factory=factory, min_angle =-90, max_angle = 90, min_pulse_width = 0.00036 , max_pulse_width = 0.00227)

    def set_platform_angle (self, pitch, roll, z):
        """
        takes in an angle 
        """
        servo_angles = get_servo_angles(pitch, roll, z)
        
        self.set_servos(servo_angles)
        
    def set_servos(self, servo_angles):
        """
        sets all the servo angles 
        """
        if MIN_ANGLE <= servo_angles[0] <= MAX_ANGLE:
            self.servo1.angle= servo_angles[0]
            #sleep(0.01)
        else:
            print("Angle 1 failed: angle = ", servo_angles[0])
            return
        if MIN_ANGLE<= servo_angles[1] <= MAX_ANGLE:
            self.servo2.angle= servo_angles[1]
            #sleep(0.01)
        else:
            print("Angle 1 failed: angle = ", servo_angles[1])
            return

        if MIN_ANGLE<= servo_angles[2] <= MAX_ANGLE:
            self.servo3.angle= servo_angles[2]
            #sleep(0.01)
        else:
            print("Angle 1 failed: angle = ", servo_angles[2])
            return
        sleep(0.2)

    def cleanup(self):
        self.servo1.close()
        self.servo2.close()
        self.servo3.close()

# if __name__ == "main":
#     p = PlatformController()

#     p.set_platform_angle(0,0,50)
#     p.set_platform_angle(0,0,90)
#     p.set_platform_angle(0,0,30)
#     sleep(10)
#     p.cleanup()