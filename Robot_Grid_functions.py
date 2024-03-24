from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *

hub = PrimeHub()
distance=DistanceSensor('C')
color_sensor=ColorSensor('D')
motor_pair=MotorPair("A","B")
class Robot:
    """ for real application
    def __init__(self, color_sensor, motor1, motor2):
        self.color_sensor = color_sensor
        self.motor1 = motor1
        self.motor2 = motor2
    """
    def __init__(self):
        self.position = (0,0)
    def go_forward():
        motor_pair.move(grid_length,unit="cm",steering=0,speed=30)
        self.position.change_position()
    def turn_left():
        motor_pair.move(0,unit='cm',steering=-100,speed=30)
    def turn_right():
        motor_pair.move(0,unit='cm',steering=100,speed=30)
    def is_facing_block():
        if get_distance_cm(short_range=True)<=appropriate_box_finding_range:
            return True
        else:
            return False
    def is_grid_red():
        color=color_sensor.get_color()
        if color =='red':
            send_current_position()
            return True
        else:
            return False
