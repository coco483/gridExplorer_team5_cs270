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

    def go_forward(self):
        self.motor_pair.move(23,unit="cm",steering=0,speed=30)
        if self.direction=='N':
            self.position=(self.position[0],self.position[1]+1)
        elif self.direction=='E':
            self.position=(self.position[0]+1,self.position[1])
        elif self.direction=='W':
            self.position=(self.position[0]-1,self.position[1])
        elif self.direction=='S':
            self.position=(self.position[0],self.position[1]-1)

    def turn_left(self):
        self.motor_pair.move(0.66,unit='rotations',steering=-100,speed=30)
        if self.direction=='N':
            self.direction='W'
        elif self.direction=='W':
            self.direction='S'     
        elif self.direction=='S':
            self.direction='E'
        elif self.direction=='E':
            self.direction='N'                               
    def turn_right(self):
        self.motor_pair.move(0.66,unit='rotations',steering=100,speed=30)
        if self.direction=='N':
            self.direction='E'
        elif self.direction=='E':
            self.direction='S'
        elif self.direction=='S':
            self.direction='W'
        elif self.direction=='W':
            self.direction='N'

    def is_grid_red(self):
        color=self.color_sensor.get_color()
        if color =='red':
            return True
        else:
            return False

    def scan_forward(self):
        if self.distance_for.get_distance_cm(short_range=False)<=130:
            number_of_grid_for=round(self.distance_for.get_distance_cm(short_range=False)/23)
            if self.direction=='N':
                box_position=(self.position[0],self.position[1]+number_of_grid_for)          
            elif self.direction=='E':
                box_position=(self.position[0]+number_of_grid_for,self.position[1])  
            elif self.direction=='W':
                box_position=(self.position[0]-number_of_grid_for,self.position[1])
            elif self.direction=='S':
                box_position=(self.position[0],self.position[1]-number_of_grid_for)
            return box_position
        else:
            return (-1,-1)
    
    def scan_side(self):
        if self.distance_side.get_distance_cm(short_range=False)<=130:
            number_of_grid_side=round(self.distance_side.get_distance_cm(short_range=False)/23)
            if self.direction=='N':
                box_position=(self.position[0]+number_of_grid_side,self.position[1])
            elif self.direction=='E':
                box_position=(self.position[0],self.position[1]-number_of_grid_side)
            elif self.direction=='W':
                box_position=(self.position[0],self.position[1]+number_of_grid_side)
            elif self.direction=='S':
                box_position=(self.position[0]-number_of_grid_side,self.position[1])
            return box_position
        else:
            return (-1,-1)

    def valid_check(self):
        if self.position[0]<0 or self.position[0]>5 or self.position[1]<0 or self.position[1]>3:
            self.position=(-1,-1)

    def go_to(self,x,y):
        dx= x-self.position[0]
        dy= y-self.position[1]

        if dx>=0:
            while self.direction!='E':
                self.turn_left()
            for i in range(dx):
                self.go_forward()
        else:
            while self.direction!='W':
                self.turn_left()
            for i in range(-dx):
                self.go_forward()
        
        if dy>=0:
            while self.direction!="N":
                self.turn_left()
            for i in range(dy):
                self.go_forward()
        else:
            while self.direction!="S":
                self.turn_left()
            for i in range(-dy):
                self.go_forward()

a=Robot()
