from os import name
import cv2 as cv
from numpy.core.fromnumeric import shape
import detect as detect
import numpy as np

txt_path = r'G:\telloDeneme\sonuclar\exp13\labels\d2'
# detect.run(weights=r'.\weights\modelle_0404\weights\best.pt',
#            source=r'.\denemeler\d2.jpg', view_img=True,save_txt=True,
#            save_crop=True,project=r'.\sonuclar',name='exp',
#            line_thickness=2)

with open(txt_path + '.txt', 'r') as f:
    d = f.readlines()
    print(d)
characters_to_remove = '\n() '

newAL = list()
for line in d:
    new_str = line
    for characters in characters_to_remove:
        new_str = new_str.replace(characters,"")
    newAL.append(new_str)

print(newAL)


print("intliszt: " + newAL[0][0])

intList = list()
for position in newAL:

    intList.append(position.split(','))
for i in range(0, len(intList)):
    #print(intList[i])
    for j in range(0, len(intList[i])):
        intList[i][j] = int(intList[i][j])
print(intList)

img = cv.imread(r'.\denemeler\d2.jpg')
dimensions = img.shape
cv.imshow('fafdsg',img)
blank_image = 255*np.ones(shape=dimensions,dtype=np.uint8)
cv.imshow('asdf',blank_image)

for point in intList:
    cv.circle(blank_image, point,6,(0,0,255), cv.FILLED)

cv.imshow('sdagasg', blank_image)

#
# image_with_rect = cv.rectangle(img=blank_image,pt1=(613, 426), pt2=(351, 438),color=(255,0,0),thickness=4)
# cv.imshow('sdfds',image_with_rect)
#image_with_dots = cv.circle(blank_image, (x,y), radius=0, color=(0, 0, 255), thickness=-1)

cv.waitKey()


