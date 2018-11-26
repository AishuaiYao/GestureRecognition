#-*- coding:utf-8 -*-
import cv2
import numpy as np

def ellipse_detect(image):
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    skinCrCbHist = np.zeros((256,256), dtype= np.uint8 )
    cv2.ellipse(skinCrCbHist ,(113,155),(23,15),43,0, 360, (255,255,255),-1)

    YCRCB = cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    (y,cr,cb)= cv2.split(YCRCB)
    skin = np.zeros(cr.shape, dtype=np.uint8)
    (x,y)= cr.shape
    for i in range(0,x):
        for j in range(0,y):
            CR= YCRCB[i,j,1]
            CB= YCRCB[i,j,2]
            if skinCrCbHist [CR,CB]>0:
                skin[i,j]= 255
    cv2.namedWindow(image, cv2.WINDOW_NORMAL)
    cv2.imshow(image, img)
    dst = cv2.bitwise_and(img,img,mask= skin)
    cv2.namedWindow("cutout", cv2.WINDOW_NORMAL)
    cv2.imshow("cutout",dst)

def cr_otsu_detect(image):
    img = cv2.imread(image, cv2.IMREAD_COLOR)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    (y, cr, cb) = cv2.split(ycrcb)
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
    _, skin = cv2.threshold(cr1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    cv2.namedWindow("image raw", cv2.WINDOW_NORMAL)
    cv2.imshow("image raw", img)
    cv2.namedWindow("image CR", cv2.WINDOW_NORMAL)
    cv2.imshow("image CR", cr1)
    cv2.namedWindow("Skin Cr+OTSU", cv2.WINDOW_NORMAL)
    cv2.imshow("Skin Cr+OTSU", skin)

    dst = cv2.bitwise_and(img, img, mask=skin)
    cv2.namedWindow("seperate", cv2.WINDOW_NORMAL)
    cv2.imshow("seperate", dst)

def crcb_range_detect(image):
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    ycrcb=cv2.cvtColor(img,cv2.COLOR_BGR2YCR_CB)
    (y,cr,cb)= cv2.split(ycrcb)

    skin = np.zeros(cr.shape,dtype= np.uint8)
    (x,y)= cr.shape
    for i in range(0,x):
        for j in range(0,y):
            if (cr[i][j]>140)and(cr[i][j])<175 and (cr[i][j]>100) and (cb[i][j])<120:
                skin[i][j]= 255
            else:
                skin[i][j] = 0
    cv2.namedWindow(image,cv2.WINDOW_NORMAL)
    cv2.imshow(image,img)
    cv2.namedWindow(image+"skin2 cr+cb",cv2.WINDOW_NORMAL)
    cv2.imshow(image+"skin2 cr+cb",skin)

    dst = cv2.bitwise_and(img,img,mask=skin)
    cv2.namedWindow("cutout",cv2.WINDOW_NORMAL)
    cv2.imshow("cutout",dst)

def hsv_detect(image):
    img = cv2.imread(image,cv2.IMREAD_COLOR)
    hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    (_h,_s,_v)= cv2.split(hsv)
    skin= np.zeros(_h.shape,dtype=np.uint8)
    (x,y)= _h.shape

    for i in range(0,x):
        for j in range(0,y):
            if(_h[i][j]>7) and (_h[i][j]<20) and (_s[i][j]>28) and (_s[i][j]<255) and (_v[i][j]>50 ) and (_v[i][j]<255):
                skin[i][j] = 255
            else:
                skin[i][j] = 0
    cv2.namedWindow(image, cv2.WINDOW_NORMAL)
    cv2.imshow(image, img)
    cv2.namedWindow(image + "hsv", cv2.WINDOW_NORMAL)
    cv2.imshow(image + "hsv", skin)
    dst = cv2.bitwise_and(img, img, mask=skin)
    cv2.namedWindow("cutout", cv2.WINDOW_NORMAL)
    cv2.imshow("cutout", dst)



# img = cv2.VideoCapture(0)
while(1):
    # ellipse_detect("hand.jpg")
    # cr_otsu_detect("hand.jpg")
    # crcb_range_detect("hand.jpg")
    hsv_detect("hand.jpg")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#
#     _,frame=img.read()
#     ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCR_CB)
#
#     (y, cr, cb) = cv2.split(ycrcb)
#     cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
#     _, skin1 = cv2.threshold(cr1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
#
#     cv2.namedWindow("image raw", cv2.WINDOW_NORMAL)
#     cv2.imshow("image raw", frame)
#     cv2.namedWindow("image CR", cv2.WINDOW_NORMAL)
#     cv2.imshow("image CR", cr1)
#     cv2.namedWindow("Skin Cr+OTSU", cv2.WINDOW_NORMAL)
#     cv2.imshow("Skin Cr+OTSU", skin1)
#
#     dst = cv2.bitwise_and(frame, frame, mask=skin1)
#     cv2.namedWindow("sperate", cv2.WINDOW_NORMAL)
#     cv2.imshow("sperate", dst)
#
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()



