import KeyboardControl as kc
from djitellopy import tello
from time import sleep
import time
import cv2

kc.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
drone.streamon()
global img


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    landOrTakeOff = 0

    if kc.getKey("LEFT"):
        lr = -speed
    elif kc.getKey("RIGHT"):
        lr = speed

    if kc.getKey("UP"):
        fb = speed
    elif kc.getKey("DOWN"):
        fb = -speed

    if kc.getKey("w"):
        ud = speed
    elif kc.getKey("s"):
        ud = -speed

    if kc.getKey("a"):
        yv = speed
    elif kc.getKey("d"):
        yv = -speed

    if kc.getKey("q"):   drone.land() ; landOrTakeOff = 1 ; sleep(1)
    if kc.getKey("e"):   drone.takeoff() ; landOrTakeOff = 1 ; sleep(1)

    if kc.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        sleep(0.3)

    return [lr, fb, ud, yv, landOrTakeOff]


while True:
    vals = getKeyboardInput()
    if vals[4] == 1: continue
    else:
        drone.send_rc_control(vals[0], vals[1], vals[2], vals[3])
        img = drone.get_frame_read().frame
        img = cv2.resize(img, (416, 416))
        #360,240
        cv2.imshow("Image", img)
        cv2.waitKey(1)
