from roboControl import Robot

##example code
if __name__ == '__main__':
    robo = Robot()
    robo.go_forward()
    if robo.is_facing_block():
        pass