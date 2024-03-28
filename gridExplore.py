from roboControl import Robot

##example code
if __name__ == '__main__':
    robo = Robot()
    box1_x, box1_y = robo.scan_forward()
    if box1_x == -1 and box1_y == -1 : 
        robo.scan_side()
        for i in range(3) :
            robo.scan_side()
            robo.move_straight()
