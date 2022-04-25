from os import name
import cv2 as cv
from numpy.core.fromnumeric import shape
import detect as detect
import numpy as np

detect.run(weights=r'.\weights\modelle_0404\weights\best.pt',
           source=r'.\denemeler\d2.jpeg', view_img=True,save_txt=True,
           save_crop=True,project=r'.\sonuclar',name='exp',
           line_thickness=5)

img = cv.imread(r'.\denemeler\d2.jpeg')
dimensions = img.shape
blank_image = 255*np.ones(shape=dimensions,dtype=np.uint8)
cv.imshow('asdf',blank_image)

image_with_rect = cv.rectangle(img=blank_image,pt1=(613, 426), pt2=(351, 438),color=(255,0,0),thickness=4)
cv.imshow('sdfds',image_with_rect)
#image_with_dots = cv.circle(blank_image, (x,y), radius=0, color=(0, 0, 255), thickness=-1)

cv.waitKey()


