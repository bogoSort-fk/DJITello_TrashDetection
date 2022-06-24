import math
import cv2 as cv
import detect as detect
import numpy as np
import geo as geo
import time

pixelToMetCoefficient   = 0.026 * 2.8 * 0.01
xDistanceToRobot        = 0.6               # distance of drone to robot
yDistanceToRobot        = 0.6
lstForRelToRobot        = [xDistanceToRobot-0.278,yDistanceToRobot-0.278]
vecRelToRobot           = np.array(lstForRelToRobot)
imageNameInExplorer     = "33"

def findRelativePositions(intList):

    vecListWithRelDistance = list()
    hypListWithRelDistance = list()
    angleListWithNormalVec = list()
    x, y            = 0, 0
    normalLst       = [0, 1]
    normalVector    = np.array(normalLst)

    for position in intList:
        x = (712 - position[0])*pixelToMetCoefficient
        y = (712 - position[1])*pixelToMetCoefficient
        lst = [x,y]
        vectorizedPos = np.array(lst) + vecRelToRobot
        vecListWithRelDistance.append(vectorizedPos)
        hypotenusRelatedToRobot = np.hypot(vectorizedPos[0],vectorizedPos[1])
        unit_vector_1 = vectorizedPos / np.linalg.norm(vectorizedPos)
        unit_vector_2 = normalVector / np.linalg.norm(normalVector)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        angle = np.arccos(dot_product)
        print(math.degrees(angle))
        angleListWithNormalVec.append(angle)
        hypListWithRelDistance.append(hypotenusRelatedToRobot)

    return vecListWithRelDistance, hypListWithRelDistance, angleListWithNormalVec


# or 0,026
# centimeters = pixels * 2.54 / 96
# because of rescaling image due to capacity of transferred data there would be another 3*
# also finding relativ distance to right bottom frame (712,712) which has a difference to
# the position of drone like (356,356), which is also nearly 27,8 cm

def positionEvaluation():

    txt_path = r'G:\telloDeneme\sonuclar\exp38\labels\33'
    newAL = list()
    characters_to_remove = '\n() '

    with open(txt_path + '.txt', 'r') as f:
        d = f.readlines()
        print(d)

    for line in d:
        new_str = line
        for characters in characters_to_remove:
            new_str = new_str.replace(characters, "")
        newAL.append(new_str)

    intList = list()
    for position in newAL:
        intList.append(position.split(','))
    for i in range(0, len(intList)):

        for j in range(0, len(intList[i])):
            intList[i][j] = int(intList[i][j])
    print(intList)

    img = cv.imread(r'.\denemeler\dist\33.jpg')
    cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    cv.imshow("th",img)
    dimensions = img.shape
    cv.imshow('Original Image', img)
    blank_image = 255 * np.ones(shape=dimensions, dtype=np.uint8)

    for point in intList:
        cv.circle(blank_image, point, 6, (0, 0, 255), cv.FILLED)

    cv.imshow('Image with dots', blank_image)
    cv.waitKey()

    return intList


def detectObjects():

    detect.run(weights=r'.\weights\modelle_1705\weights\best.pt',
               source=r'.\denemeler\dist', view_img=True,save_txt=True,
               save_crop=True,project=r'.\sonuclar',name='exp',
               line_thickness=2)

# detectObjects()
intList = positionEvaluation()
vectorsOfRelativeDistance, hypsOfDistance, angleBetweenNormalVec = findRelativePositions(intList)
print(hypsOfDistance)

txtPathForWP = f'./waypoint{time.time()}'
wpListWithLatLang = list()



for i in range(0, len(vectorsOfRelativeDistance)):
    latOfWaypoint, langOfWaypoint = geo.distanceBearing(41.144609, 29.100827, hypsOfDistance[i], 250-angleBetweenNormalVec[i])
    wpListWithLatLang.append([latOfWaypoint,langOfWaypoint])

print(wpListWithLatLang[0])

with open(txtPathForWP + '.txt', 'a') as f:
    f.write("QGC WPL 110\n")
    for i in range(0, len(wpListWithLatLang)):
        latOfWaypoint  = wpListWithLatLang[i][0]
        langOfWaypoint = wpListWithLatLang[i][1]
        if i == 0:
            f.write(str(i) + "  " + "1" + "   " + "0" + "   " + "16" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "41.144609" +
                "   " + "29.100827" + "   " + "0" + "   " + "1")
            f.write("\n")
            f.write(str(i+1) + "  " + "0" + "   " + "3" + "   " + "16" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + f"{latOfWaypoint}" +
                "   " + f"{langOfWaypoint}" + "   " + "0" + "   " + "1")
            f.write("\n")
        elif i+1 == len(vectorsOfRelativeDistance):
            f.write(str(i+1) + "  " + "0" + "   " + "3" + "   " + "16" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + f"{latOfWaypoint}" +
                "   " + f"{langOfWaypoint}" + "   " + "0" + "   " + "1")
            f.write("\n")
            f.write(str(i+2) + "  " + "0" + "   " + "3" + "   " + "20" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "0.0" +
                "   " + "0.0" + "   " + "0.0" + "   " + "1")
            f.write("\n")
        else:
            f.write(str(i+1) + "  " + "0" + "   " + "3" + "   " + "16" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + "0" + "   " + f"{latOfWaypoint}" +
                "   " + f"{langOfWaypoint}" + "   " + "0" + "   " + "1")
            f.write("\n")










