from cs1robots import *
import time

n = int(input("test map number(1-11): "))
while (n<1 or n>11):
  print("not a valid num")
  n = input("test map number(1-11): ")

load_world(f"./testRobo/worlds/amazing{n}.wld")

class CustomRobot(Robot):
  def __init__(self, xpos, ypos):
    self.hubo = Robot()
    self.hubo.set_trace("blue")
    self.hubo.turn_left()
    self.position=(0,0)
    self.red=set()
    self.visited_list = set()
    self.boxes=[]
    self.direction='N'
    self.leftCount = 0
    self.rightCount= 0
    self.safe_columns=[0,1,2,3,4,5]
    self.safe_rows=[0,1,2,3]

  
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
    self.is_grid_red()
    self.visited_list.add(self.position)

  def go_back(self):
    (templ, tempr) = (self.leftCount, self.rightCount)
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
    (self.leftCount, self.rightCount) = (templ, tempr)
    self.is_grid_red()
    self.visited_list.add(self.position)

  def turn_left(self):
    print("turnleft called")
    self.leftCount +=1
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
    print("turnright called")
    self.rightCount+=1
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
      self.red.add(self.position)
      return True
    return False

  def scan_forward(self):
    (templ, tempr) = (self.leftCount, self.rightCount)
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
      (self.leftCount, self.rightCount) = (templ, tempr)
      return boxpos
    for i in range(count):
      self.go_back()
    print("(-1, -1)")
    (self.leftCount, self.rightCount) = (templ, tempr)
    return (-1, -1)
  
    
  def scan_side(self):
    (templ, tempr) = (self.leftCount, self.rightCount)
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
      (self.leftCount, self.rightCount) = (templ, tempr)
      return boxpos
    for i in range(count):
      self.go_back()
    self.turn_left()
    print("scan side: -1 -1")
    (self.leftCount, self.rightCount) = (templ, tempr)
    return (-1, -1)

  def valid_check(self):
    if self.position[0]<0 or self.position[0]>5 or self.position[1]<0 or self.position[1]>3:
      self.position=(-1,-1)

  def go_to2(self,x,y):
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

  def go_to(self,x,y):
      print("goto", x, y)
      dx= x-self.position[0]
      dy= y-self.position[1]

      if dx !=0:
          if self.direction == "N":
              self.turn_right()
          elif self.direction == "S":
              self.turn_left()
          elif self.direction == "W":
              dx = -dx
          if dx>0:
              for i in range(dx):
                  self.go_forward()
          elif dx <0:
              for i in range(-dx):
                  self.go_back()
      if dy !=0:
          if self.direction == "E":
              self.turn_left()
          elif self.direction == "W":
              self.turn_right()
          elif self.direction == "S":
              dy = -dy
          if dy>0:
              for i in range(dy):
                  self.go_forward()
          elif dy <0:
              for i in range(-dy):
                  self.go_back()
  '''
  def update_safe_columns(self):
        #두 박스가 존재하지 않는 column number들을 업데이트
        for i in range(2):
            self.safe_columns.remove(boxes[i][0])
  def update_safe_rows(self):
      #두 박스가 존재하지 않는 row number 들을 업데이트
      for i in range(2):
          self.safe_rows.remove(boxes[i][1])
  def check_column(self):
        #위쪽을 바라보며 시작
        self.is_grid_red()
        for i in range(3):
            self.go_forward()
            self.is_grid_red()
        for i in range(3):
            self.go_back()
  def check_row(self):
      #오른쪽을 바라보며 시작
      self.is_grid_red()
      for i in range(5):
          self.go_forward()
          self.is_grid_red()
      for i in range(5):
          self.go_back()

  def go_to_column(self, n,m):
      #(n,0)에서 (m,0)으로 이동 (safe row 를 따라서 이동하고 내려옴) 시작할때 위를 바라보고 도착하고 위를 바라봄

      smallest_safe_row=min(self.safe_rows)
      for i in range(smallest_safe_row):
          self.go_forward()
      self.turn_right()
      for i in range(m-n):
          self.go_forward()
      self.turn_left()
      for i in range(smallest_safe_row):
          self.go_back()
  

  def go_to_row(self,n,m):
      #(0,n)에서 (0,m)으로 이동 (safe columns 을 따라서 이동하고 왼쪽으로 옴) 시작할때오른쪽을 바라보고 도착하고 오른쪽을 바라봄
      smallest_safe_column=min(self.safe_columns)
      for i in range(smallest_safe_column):
          self.go_forward()
      self.turn_left()
      for i in range(m-n):
          self.go_forward()
      self.turn_right()
      for i in range(smallest_safe_row):
          self.go_back()    

  def go_back_to_origin_column(self,n):
      #(n,0)에서 (0,0)으로 safe row를 따라서 이동(출발할때 도착할때 위를 바라봄)
      smallest_safe_row=min(self.safe_rows)
      for i in range(smallest_safe_row):
          self.go_forward()
      self.turn_right()
      for i in range(n):
          self.go_back()
      self.turn_left()
      for i in range(smallest_safe_row):
          self.go_back()
      
  def go_back_to_origin_row(self, n):
      smallest_safe_column=min(self.safe_columns)
      for i in range(smallest_safe_row):
          self.go_forward()
      self.turn_left()
      for i in range(n):
          self.go_back()
      self.turn_right()
      for i in range(smallest_safe_row):
          self.go_back()

  '''




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
    if b2_x != -1 and b2_y != -1 :
        pass

    else :
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
                if b2_x == b1_x and b2_y == b1_y :
                    b2_x, b2_y = (-1, -1)
            for i in range(3) :
                robo.go_forward()
            robo.turn_right()
        for i in range(5) :
            robo.go_forward()
        robo.turn_right()
print(b1_x,b1_y,b2_x,b2_y)

red_pos = []
visited_list = [(0, 0)]

def dfs_stack(start_pos):
    # 주어진 위치에서 갈 수 있는 좌표를 출력, 없으면 빈 리스트를 출력한다
    def get_possible_move(cur_pos):
        res = []

        for (dx, dy) in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
            candidate = (cur_pos[0]+dx, cur_pos[1]+dy)

            # 맵을 벗어남
            if not 0 <= candidate[0] <= 5 or not 0 <= candidate[1] <= 3: continue

            # 왔던 길은 다시 탐색하지 않음
            if candidate in visited: continue

            # 장애물이 있어 갈 수 없음
            if candidate == (b1_x, b1_y) or candidate == (b2_x, b2_y): continue

            res.append(candidate)

        return res


    # robo.go_to의 helper function
    def goto(dest):
        robo.go_to(dest[0], dest[1])


    visited = set() # 방문한 곳을 집합에 저장
    stack = [start_pos] # 앞으로 갈 곳을 스택에 저장
    route = [start_pos] # 지나온 길을 저장

    while len(stack) > 0 and len(red_pos) < 2:
        #print(f'[debug]\nred: {red_pos}\nstack: {stack}\nroute: {route}')
        current_pos = stack.pop()
        if not robo.position == current_pos:
            goto(current_pos)
            route.append(current_pos)

        visited.add(current_pos)
        # 현재 위치가 스택에 있을 경우 삭제
        if current_pos in stack:
            stack = [x for x in stack if x != current_pos]

        if robo.is_grid_red():
            red_pos.append(current_pos)
            if len(red_pos) == 2: break

        possible_move = get_possible_move(current_pos)

        if len(possible_move) == 0: # 현재 위치에서 더 이상 갈 수 있는 곳이 존재하지 않음
            while len(get_possible_move(current_pos)) == 0:
                current_pos = route.pop()
                goto(current_pos)

            # 현재 위치를 route에 다시 넣어줌
            route.append(current_pos)
        else: # 현재 위치에서 갈 수 있는 곳이 존재함
            for next_pos in possible_move:
                stack.append(next_pos)

    # 모든 red cell을 찾았으므로 귀환
    while len(route) > 0:
        dest = route.pop()
        goto(dest)


dfs_stack((0, 0))


print("b1 is ", b1_x, b1_y, "and b2 is", b2_x, b2_y)
print(red_pos)
print("turn count", robo.leftCount, robo.rightCount)

#print(robo.red)
#print(robo.boxes)

### correct outputs
# 1: (1, 1, B) (4, 2, B) (3, 0, R) (2, 3, R)
# 2: (2, 0, B) (1, 1, B) (2, 1, R) (5, 3, R)
# 3: (1, 1, B) (4, 1, B) (2, 0, R) (3, 0, R)
# 4: (2, 0, B) (3, 3, B) (5, 0, R) (4, 3, R)
# 5: (2, 3, B) (4, 3, B) (3, 3, R) (5, 3, R)
# 6: (5, 1, B) (4, 2, B) (0, 0, R) (1, 2, R)
