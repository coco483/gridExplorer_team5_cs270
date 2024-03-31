from cs1robots import *
import time

n = int(input("test map number(1-5): "))
while (n<1 or n>5):
  print("not a valid num")
  n = input("test map number(1-5): ")

load_world(f"./testRobo/worlds/amazing{n}.wld")

class CustomRobot(Robot):
  def __init__(self, xpos, ypos):
    self.hubo = Robot()
    self.hubo.set_trace("blue")
    self.hubo.turn_left()
    self.position=(0,0)
    self.red=[]
    self.boxes=[]
    self.direction='N'
  
  def go_forward(self):
    self.hubo.move()
    if self.direction =='N':
        self.position=(self.position[0],self.position[1]+1)
    elif self.direction=='E':
        self.position=(self.position[0]+1,self.position[1])
    elif self.direction=='W':
        self.position=(self.position[0]-1,self.position[1])
    elif self.direction=='S':
        self.position=(self.position[0],self.position[1]-1)

  def go_back(self):
    self.hubo.turn_left()
    self.hubo.turn_left()
    self.hubo.move()
    self.hubo.turn_left()
    self.hubo.turn_left()
    if self.direction =='N':
        self.position=(self.position[0],self.position[1]-1)
    elif self.direction=='E':
        self.position=(self.position[0]-1,self.position[1])
    elif self.direction=='W':
        self.position=(self.position[0]+1,self.position[1])
    elif self.direction=='S':
        self.position=(self.position[0],self.position[1]+1)

  def turn_left(self):
    #print("turnleft called")
    self.hubo.turn_left()
    if self.direction=='N':
        self.direction='W'
    elif self.direction=='W':
        self.direction='S'     
    elif self.direction=='S':
        self.direction='E'
    elif self.direction=='E':
        self.direction='N'

  def turn_right(self):
    #print("turnright called")
    self.hubo.turn_left()
    self.hubo.turn_left()
    self.hubo.turn_left()
    if self.direction=='N':
        self.direction='E'
    elif self.direction=='E':
        self.direction='S'
    elif self.direction=='S':
        self.direction='W'
    elif self.direction=='W':
        self.direction='N'

  def is_grid_red(self):
    if self.hubo.on_beeper():
      self.red.append(self.position)
      return True
    return False

  def scan_forward(self):
    count = 0
    while(self.hubo.front_is_clear()):
      self.go_forward()
      count+=1
    #print(self.position)
    if self.direction=='N':
      boxpos = (self.position[0], self.position[1]+1)
    elif self.direction=='W':
      boxpos = (self.position[0]-1, self.position[1])     
    elif self.direction=='S':
      boxpos = (self.position[0], self.position[1]-1)
    elif self.direction=='E':
      boxpos = (self.position[0]+1, self.position[1])
    if (boxpos[0] < 5) and (boxpos[0]>=0) and (boxpos[1]>=0) and (boxpos[1] <3):
      for i in range(count):
        self.go_back()
      print(boxpos)
      self.boxes.append(boxpos)
      return boxpos
    for i in range(count):
      self.go_back()
    print("(-1, -1)")
    return (-1, -1)
  
    
  def scan_side(self):
    count = 0
    self.turn_right()
    while(self.hubo.front_is_clear()):
      self.go_forward()
      count+=1
    #print("position: ", end="")
    #print(self.position)
    if self.direction=='N':
      boxpos = (self.position[0], self.position[1]+1)
    elif self.direction=='W':
      boxpos = (self.position[0]-1, self.position[1])     
    elif self.direction=='S':
      boxpos = (self.position[0], self.position[1]-1)
    elif self.direction=='E':
      boxpos = (self.position[0]+1, self.position[1])
    if (boxpos[0] <= 5) and (boxpos[0]>=0) and (boxpos[1]>=0) and (boxpos[1] <=3):
      for i in range(count):
        self.go_back()
      self.turn_left()
      self.boxes.append(boxpos)
      print("boxpos: ", end="")
      print(boxpos)
      return boxpos
    for i in range(count):
      self.go_back()
    self.turn_left()
    print("scan side: -1 -1")
    return (-1, -1)

  def valid_check(self):
    if self.position[0]<0 or self.position[0]>5 or self.position[1]<0 or self.position[1]>3:
      self.position=(-1,-1)

  def goto(self,x,y):
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


robo = CustomRobot(0,0)
#robo.set_trace("blue")

### hubo methods
# hubo.move()
# hubo.turn_left()
# hubo.set_pause(2)
# hubo.on_beeper() - red cell
# hubo.front_is_clear() - box (hubo cannot distinguish end of map and box walls)

### implement here




print("b1 is ", b1_x, b1_y, "and b2 is", b2_x, b2_y)


#print(robo.red)
#print(robo.boxes)

### correct outputs
# 1: (1, 1, B) (4, 2, B) (3, 0, R) (2, 3, R)
# 2: (2, 0, B) (1, 1, B) (2, 1, R) (5, 3, R)
# 3: (1, 1, B) (4, 1, B) (2, 0, R) (3, 0, R)
# 4: (2, 0, B) (3, 3, B) (5, 0, R) (4, 3, R)
# 5: (5, 1, B) (4, 2, B) (0, 0, R) (1, 2, R)