# -*- coding:utf-8 -*-
#背景差法需要安装opencv-contrib-python模块才能使用

import cv2
import numpy as np
import time
import skindetection as sd
import motiondetection as md

camera = cv2.VideoCapture(0)
#camera = cv2.VideoCapture("../video/2.mp4")

# fgbg1 = cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg2 = cv2.createBackgroundSubtractorMOG2()
# fgbg3 = cv2.bgsegm.createBackgroundSubtractorGMG(60)  # initializationFrames=120
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

freq_aver=0
freq=[]
sd_mask = np.zeros((64,64), dtype=np.uint8)

cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
# cv2.namedWindow("hand", cv2.WINDOW_NORMAL)

while 1:
    begin = time.time()
    ret, frame = camera.read()
    if ret is True:
        fgmask,ROI = md.backgrounddifference(frame,fgbg2,kernel)
        roi = cv2.resize(ROI.copy(), (64, 64), interpolation=cv2.INTER_LINEAR)

        # sd_mask= sd.ellipse_detect(roi)
        # sd_mask = sd.cr_otsu(roi)
        sd_mask= sd.crcb_range_sceening(roi)
        # sd_mask = sd.hsv_detect(roi)

        sd_mask = cv2.morphologyEx(sd_mask, cv2.MORPH_OPEN, kernel, iterations=1)
        hand=cv2.bitwise_and(roi, roi, mask=sd_mask)
        cv2.putText(frame, ("FPS:" + str(round(freq_aver, 3)) + "ms"), (20, 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,
                    (0, 0, 255),1,1)
        cv2.imshow("frame", frame)
        cv2.imshow("mask", fgmask)
        cv2.imshow("ROI", ROI)
        cv2.imshow("hand", hand)
        cv2.waitKey(1)
    else:
        print "playing is over"
        cv2.destroyAllWindows()
        camera.release()
        break
    end = time.time()
    freq.append(end-begin)
    if len(freq)>9:
        freq_aver= sum(freq)/10
        freq.pop()
        print freq_aver



































