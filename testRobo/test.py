from cs1robots import *
import time

n = int(input("test map number(1-10): "))
while (n<1 or n>10):
  print("not a valid num")
  n = input("test map number(1-10): ")

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


robo = CustomRobot(0,0)
#robo.set_trace("blue")

### hubo methods
# hubo.move()
# hubo.turn_left()
# hubo.set_pause(2)
# hubo.on_beeper() - red cell
# hubo.front_is_clear() - box (hubo cannot distinguish end of map and box walls)

### implement here
b1_x, b1_y = robo.scan_forward()
b2_x, b2_y = (-1, -1)

if b1_x == -1 and b1_y == -1 : 
    b1_x, b1_y = robo.scan_side()
    for i in range(3) :
        robo.go_forward()
        if b1_x != -1 and b1_y != -1 :
            if b2_x < 0 and b2_y < 0 :
                b2_x, b2_y = robo.scan_side()
        else :
            b1_x, b1_y = robo.scan_side()

    if b2_x == -1 and b2_y == -1 :
        if b1_y == 3 :
            for i in range(3) :
                robo.go_back()
            robo.turn_left()
            for i in range(5) :
                robo.go_back()
                if b2_x < 0 and b2_y < 0 :
                    b2_x, b2_y = robo.scan_side()
                if b2_x == b1_x :
                    b2_x, b2_y = (-1, -1)
            for i in range(5) :
                robo.go_forward()
            robo.turn_right()
        
        else :
            robo.turn_right()
            for i in range(5) :
                robo.go_forward()
                if b2_x < 0 and b2_y < 0 :
                    b2_x, b2_y = robo.scan_side()
                if b2_x == b1_x :
                    b2_x, b2_y = (-1, -1)
            for i in range(5) :
                robo.go_back()
            robo.turn_left()
            for i in range(3) :
                robo.go_back()
    
    else :
        for i in range(3) :
            robo.go_back()

else :
    robo.scan_side()
    if b2_x == -1 and b2_y == -1 :
        robo.turn_left()
        for i in range(5) :
            robo.go_back()
            if b2_x < 0 and b2_y < 0 :
                b2_x, b2_y = robo.scan_side()
        if b2_x < 0 and b2_y < 0 :
            robo.turn_left()
            for i in range(3) :
                robo.go_back()
                if b2_x < 0 and b2_y < 0 :
                    b2_x, b2_y = robo.scan_side()
                if (b2_x, b2_y) == (b1_x, b1_y) :
                    b2_x, b2_y = (-1, -1)
            for i in range(3) :
                robo.go_forward()
            robo.turn_right()
        for i in range(5) :
            robo.go_forward()
        robo.turn_right()

red_pos = []
visited_list = [(0, 0)]

def dfs(prev_pos):
    visited_list.append(robo.position)

    # 현재 위치가 red grid인지 먼저 확인
    if robo.is_grid_red():
        red_pos.append(robo.position)

        # 모든 red grid를 탐색 완료함: 즉시 탐색을 중지하고 dfs 재귀를 회수하며 초기 위치로 돌아감
        if len(red_pos) == 2: 
            if not prev_pos == (-1, -1): robo.go_to(prev_pos[0], prev_pos[1])
            return True

    possible_move = []
    for (dx, dy) in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
        candidate_dest = (robo.position[0]+dx, robo.position[1]+dy)

        # 맵을 벗어남
        if not 0 <= candidate_dest[0] <= 5 or not 0 <= candidate_dest[1] <= 3: continue 

        # 왔던 길은 다시 탐색하지 않음
        if candidate_dest in visited_list: continue 

        # 장애물이 있어 갈 수 없음
        if candidate_dest == (b1_x, b1_y) or candidate_dest == (b2_x, b2_y): continue

        possible_move.append(candidate_dest)

    while len(possible_move) > 0:
        new_prev_pos = tuple(robo.position)
        dest = possible_move.pop()
        print("dest: ", dest, "current: ", new_prev_pos, "pos: ", robo.position)
        #time.sleep(2)
        robo.go_to(dest[0], dest[1])
        
        dfs(new_prev_pos)

        # 모든 red grid를 탐색 완료함: 즉시 탐색을 중지하고 dfs 재귀를 회수하며 초기 위치로 돌아감
        if len(red_pos) == 2: break

    # 모든 이동 가능한 위치를 다 돌아봄(갈 수 있는 선택지가 없음): 다시 원래 위치로 되돌아감
    if not prev_pos == (-1, -1): 
      print("while end", prev_pos)
      robo.go_to(prev_pos[0], prev_pos[1])
    return True
print("b1 is ", b1_x, b1_y, "and b2 is", b2_x, b2_y)
# 실행
dfs((-1, -1))


print("b1 is ", b1_x, b1_y, "and b2 is", b2_x, b2_y)
print(red_pos)

#print(robo.red)
#print(robo.boxes)

### correct outputs
# 1: (1, 1, B) (4, 2, B) (3, 0, R) (2, 3, R)
# 2: (2, 0, B) (1, 1, B) (2, 1, R) (5, 3, R)
# 3: (1, 1, B) (4, 1, B) (2, 0, R) (3, 0, R)
# 4: (2, 0, B) (3, 3, B) (5, 0, R) (4, 3, R)
# 5: (2, 3, B) (4, 3, B) (3, 3, R) (5, 3, R)
# 6: (5, 1, B) (4, 2, B) (0, 0, R) (1, 2, R)
