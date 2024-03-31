from roboControl import Robot

robo = Robot()
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
                if b2_x == b1_x :
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
            if not prev_pos == (-1, -1): robo.goto(prev_pos)
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

        robo.go_to(dest[0], dest[1])
        dfs(new_prev_pos)

        # 모든 red grid를 탐색 완료함: 즉시 탐색을 중지하고 dfs 재귀를 회수하며 초기 위치로 돌아감
        if len(red_pos) == 2: break

    # 모든 이동 가능한 위치를 다 돌아봄(갈 수 있는 선택지가 없음): 다시 원래 위치로 되돌아감
    if not prev_pos == (-1, -1): robo.go_to(prev_pos[0], prev_pos[1])
    return True

# 실행
dfs((-1, -1))
