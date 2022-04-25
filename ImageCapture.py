from djitellopy import tello
from time import sleep
import cv2

drone = tello.Tello()
drone.connect()
drone.connect(drone.get_battery())

drone.streamon()

while True:
    img = drone.get_frame_read().frame
    img = cv2.resize(img,(360,240))
    cv2.imshow("Image",img)
    cv2.waitKey(1)

