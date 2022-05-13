import cv2 as cv
import numpy as np

def Preprocessing (image,alpha,beta,gamma):

    new_img = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
    lookUpTable = np.empty((1, 256), np.uint8)
    for i in range(256):
        lookUpTable[0, i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)
    res = cv.LUT(new_img, lookUpTable)

    return res



# try:
#     alpha = float(input('* Enter the alpha value [1.0-3.0]: '))
#     beta = int(input('* Enter the beta value [0-100]: '))
#     gamma = float(input('* Enter the gamma value [0-25.0]: '))
# except ValueError:
#     print('Error, not a number')
def nothing(x):
    pass
if __name__ == '__main__':
    image = cv.imread(r'.\denemeler\kkk.jpg')
    cv.imshow('Img', image)
    cv.namedWindow('image')

    cv.createTrackbar('Alpha','image',1,3,nothing)
    cv.createTrackbar('Beta','image',0,100,nothing )
    cv.createTrackbar('Gamma','image',0,10,nothing )
    while(1):
        a=cv.getTrackbarPos('Alpha', 'image')
        b=cv.getTrackbarPos('Beta', 'image')
        g=cv.getTrackbarPos('Gamma', 'image')
        res = Preprocessing(image,a,b,g)
        cv.imshow('After gamma', res)
        cv.waitKey()



# cv.imshow('Original Image', image)
# cv.imshow('After Preprocessing', new_img)
