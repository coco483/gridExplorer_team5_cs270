from roboControl import Robot

robo = Robot()
b1_x, b1_y = robo.scan_forward()
b2_x, b2_y = (0, 0)

if b1_x == -1 and b1_y == -1 : 
    b1_x, b1_y = robo.scan_side()
    for i in range(3) :
        robo.go_forward()
        if b1_x != -1 and b1_y != -1 :
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
                b2_x, b2_y = robo.scan_side()
        
        else :
            robo.turn_right()
            for i in range(5) :
                robo.go_forward()
                b2_x, b2_y = robo.scan_side()
    
    else :
        pass

else :
    robo.scan_side()
    if b2_x != -1 and b2_y != -1 :
        if b1_y == 1 :
            robo.turn_right()
            robo.go_forward()
            robo.turn_left()
            robo.go_forward()
        else :
            robo.go_forward()
            robo.turn_right()
            robo.go_forward()
            robo.turn_left()
        
    else :
        robo.turn_left()
        for i in range(5) :
            robo.go_back()
            b2_x, b2_y = robo.scan_side()
