from djitellopy import tello
from time import sleep

drone = tello.Tello()
drone.connect()
drone.connect(drone.get_battery())

