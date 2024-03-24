from cs1robots import *
import time

n = int(input("test map number(1-5): "))
while (n<1 or n>5):
  print("not a valid num")
  n = input("test map number(1-5): ")

load_world(f"./testRobo/worlds/amazing{n}.wld")
hubo = Robot()
hubo.set_trace("blue")

### hubo methods
# hubo.move()
# hubo.turn_left()
# hubo.set_pause(2)
# hubo.on_beeper() - red cell
# hubo.front_is_clear() - box (hubo cannot distinguish end of map and box walls)


### implement here


### correct outputs
# 1: (1, 1, B) (4, 2, B) (3, 0, R) (2, 3, R)
# 2: (2, 0, B) (1, 1, B) (2, 1, R) (5, 3, R)
# 3: (1, 1, B) (4, 1, B) (2, 0, R) (3, 0, R)
# 4: (2, 0, B) (3, 3, B) (5, 0, R) (4, 3, R)
# 5: (5, 1, B) (4, 2, B) (0, 0, R) (1, 2, R)