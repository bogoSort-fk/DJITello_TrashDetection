from djitellopy import  tello
import KeyboardControl as kc
from time import sleep
import time
import numpy as np
import cv2
import math

fSpeed      = 11.7*3                  # Forward Speed in cm/s
aSpeed      = 36                    # Angular Speed in deg/s
interval    = 0.25                  # Interval to check the drone position for mapping
a           = 0                     
yaw         = 0
dInterval   = fSpeed * interval     # Distance change per unit time
aInterval   = aSpeed * interval     # Angle change per unit time
x           = 213
y           = 213
points      = [(0,0), (0,0)]
global img

kc.init()
me = tello.Tello()
me.connect()
me.streamon()
print(me.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 45
    aspeed = 50
    global x, y, yaw, a

    d = 0

    if kc.getKey("LEFT"):

        lr  = -speed
        d   = dInterval
        a   = -180

    elif kc.getKey("RIGHT"):

        lr  = speed
        d   = -dInterval
        a   = 180

    if kc.getKey("UP"):

        fb = speed
        d = dInterval
        a = 270

    elif kc.getKey("DOWN"):

        fb = -speed
        d = -dInterval
        a = -90

    if kc.getKey("w"):
        ud = speed
    elif kc.getKey("s"):
        ud = -speed

    if kc.getKey("a"):
        yv = -aspeed
        yaw -= aInterval

    elif kc.getKey("d"):
        yv = aspeed
        yaw += aInterval

    if kc.getKey("q"):   me.land()  ; sleep(1)
    if kc.getKey("e"):   me.takeoff()

    if kc.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)

    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d * math.sin(math.radians(a)))


    return [lr,fb,ud,yv,x,y]

def drawPoints(map, points):

    for point in points:
        cv2.circle(map, point, 6, (0,0,255), cv2.FILLED)
    cv2.circle(map, points[-1], 10, (0, 255, 0), cv2.FILLED)
    cv2.putText(map, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m',
                (points[-1][0]+10, points[-1][1]+30), cv2.FONT_HERSHEY_PLAIN,1,
                (255,0,255), 1)




while True:

    vals = getKeyboardInput()

    print(vals)
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])

    map = np.zeros((416,416,3), np.uint8)
    if(points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))

    drawPoints(map, points)
    # if(kc.getKey("z")):
    #     pointOfCamPerspective = points[-1][0], points[-1][1]
    # cv2.imshow("Map" , map)
    img = me.get_frame_read().frame
    me.set_video_direction(0)
    img = cv2.resize(img, (320, 240))
    # 360,240
    cv2.imshow("Image", img)
    cv2.waitKey(1)