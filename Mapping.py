from djitellopy import  tello
import KeyboardControl as kc
from time import sleep
import time
import numpy as np
import cv2
import math

fSpeed      = 117/10
aSpeed      = 360/10
interval    = 0.25
a           = 0
yaw         = 0
dInterval   = fSpeed * interval
aInterval   = aSpeed * interval
x           = 500
y           = 500
points      = [(0,0), (0,0)]
global img

kc.init()
me = tello.Tello()
me.connect()
print(me.get_battery())

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    aspeed = 50
    global x, y, yaw, a

    d = 0

    if kc.getKey("LEFT"):
        print(f"left {-speed}")
        lr  = -speed
        d   = dInterval
        a   = -180

    elif kc.getKey("RIGHT"):
        print(f"right {speed}")
        lr  = speed
        d   = -dInterval
        a   = 180

    if kc.getKey("UP"):
        print(f"up {speed}")
        fb = speed
        d = dInterval
        a = 270

    elif kc.getKey("DOWN"):
        print(f"down {-speed}")
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
    if kc.getKey("e"):   me.takeoff()  ; sleep(1)

    if kc.getKey("z"):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        sleep(0.3)

    sleep(0.25)
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

    map = np.zeros((1000,1000,3), np.uint8)
    if(points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))

    drawPoints(map, points)
    cv2.imshow("Map" , map)
    #img = me.get_frame_read().frame
    #img = cv2.resize(img, (416, 416))
    # 360,240
    #cv2.imshow("Image", img)
    cv2.waitKey(1)