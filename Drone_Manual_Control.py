import KeyboardControl as kc
from djitellopy import tello
from time import sleep
import time
import cv2
import math

kc.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
#drone.streamon()
x, y, z, r = 0, 0, 0, 0         #defines the destination

global img


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 45
    u = False
    # landOrTakeOff = 0
    global x,y,z,r

    if kc.getKey("LEFT"):
        lr = -speed
        x -= speed
    elif kc.getKey("RIGHT"):
        lr = speed
        x += speed
    if kc.getKey("UP"):
        # forward
        fb = speed
        y += speed
    elif kc.getKey("DOWN"):
        # backward
        fb = -speed
        y -= speed

    if kc.getKey("w"):
        ud = speed
        z += speed
    elif kc.getKey("s"):
        ud = -speed
        z -= speed

    if kc.getKey("a"):
        yv = speed
        r += speed
    elif kc.getKey("d"):
        yv = -speed
        r -= speed

    if kc.getKey("q"):   drone.land()
    if kc.getKey("e"):   drone.takeoff() ; z+= 80
    if kc.getKey("u"):   u = True

    if kc.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        sleep(0.3)

    sleep(0.25)
    return [lr, fb, ud, yv, u]

def deneme(x,y,z):
    drone.takeoff()
    absHeight = abs(80-x)
    if z > 0:
        drone.move_up(absHeight)
    elif z < 0:
        drone.move_down(absHeight)
    if x > 0:
        drone.move_right(x)
    elif x < 0:
        drone.move_left(x)
    if y > 0:
        drone.move_forward(y)
    elif y < 0:
        drone.move_back(y)

    drone.land()

while True:
    vals = getKeyboardInput()
    drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    #img = drone.get_frame_read().frame
    #drone.set_video_direction(0)
    print("Current height is: " + str(drone.get_height()))
    #img = cv2.resize(img, (712, 712))
    print("Current distance difference is: "+ "x :" + str(x) + "y :" + str(y)+"z :"+str(z))
    #360,240

    #cv2.imshow("Image", img)

    if vals[4] == True:
        deneme(x,y,z)
    cv2.waitKey(1)
