from spike import PrimeHub, LightMatrix, Button, StatusLight, ForceSensor, MotionSensor, Speaker, ColorSensor, App, DistanceSensor, Motor, MotorPair
from spike.control import wait_for_seconds, wait_until, Timer
from math import *
import math
hub = PrimeHub()
'''
distance_for=DistanceSensor('C')
distance_side=DistanceSensor('E')
color_sensor=ColorSensor('D')
motor_pair=MotorPair("A","B")
'''

class Robot:
    def __init__(self):
        self.motor_pair = MotorPair("B","C")
        self.color_sensor=ColorSensor("A")
        self.distance_for=DistanceSensor('D')
        self.distance_side=DistanceSensor("F")
        self.position=(0,0)
        self.red=[]
        self.boxes=[]
        self.direction='N'

    def go_forward():
        self.motor_pair.move(23,unit="cm",steering=0,speed=30)
        if self.direction=='N':
            self.position=(self.position[0],self.position[1]+1)
        elif self.direction=='E':
            self.position=(self.position[0]+1,self.position[1])
        elif self.direction=='W':
            self.position=(self.position[0]-1,self.position[1])
        elif self.direction=='S':
            self.position=(self.position[0],self.position[1]-1)

    def turn_left():
        self.motor_pair.move(0,unit='cm',steering=-100,speed=30)
        if self.direction=='N':
            self.direction=='W'
        elif self.direction=='W':
            self.direction=='S'     
        if self.direction=='S':
            self.direction=='E'
        if self.direction=='E':
            self.direction=='N'                               
    def turn_right():
        self.motor_pair.move(0,unit='cm',steering=100,speed=30)
        if self.direction=='N':
            self.direction=='E'
        elif self.direction=='E':
            self.direction=='S'
        if self.direction=='S':
            self.direction=='W'
        if self.direction=='W':
            self.direction=='N'

    def is_grid_red():
        color=self.color_sensor.get_color()
        if color =='red':
            self.red+=self.position

    def scan_forward():
        if self.distance_for.get_distance_cm(short_range=True)<=130:
            number_of_grid_for=math.round(self.distance_for.get_distance_cm(short_range=True)/23)
            box_position=(self.position[0]+number_of_grid_for,self.position[1])
            return box_position
        else:
            return (-1,-1)
    
    def scan_side():
        if self.distance_side.get_distance_cm(short_range=True)<=130:
            number_of_grid_side=math.round(self.distance_side.get_distance_cm(short_range=True)/23)
            box_position=(self.position[0],self.position[1]+number_of_grid_side)
            return box_position
        else:
            return (-1,-1)

    def valid_check():
        if self.position[0]<0 or self.position[0]>5 or self.position[1]<0 or self.position[1]>3:
            self.position=(-1,-1)
