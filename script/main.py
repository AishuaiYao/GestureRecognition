# -*- coding:utf-8 -*-
import cv2
import numpy as np
import time
import skindetection as sd
import motiondetection as md

#camera = cv2.VideoCapture(0)
camera = cv2.VideoCapture("../video/1.mp4")

# fgbg= cv2.bgsegm.createBackgroundSubtractorMOG()
fgbg = cv2.createBackgroundSubtractorMOG2()

# fgbg = cv2.bgsegm.createBackgroundSubtractorGMG(60)  # initializationFrames=120
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))

freq_aver=1
freq=[]
sd_mask = np.zeros((64,64), dtype=np.uint8)


cv2.namedWindow("frame", cv2.WINDOW_NORMAL)
cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
# cv2.namedWindow("hand", cv2.WINDOW_NORMAL)

while 1:
    begin = time.time()
    ret, frame = camera.read()
    if ret is True:
        fgmask,ROI = md.backgrounddifference(frame,fgbg)
        if ROI is not None:
            roi=ROI.copy()
        else:
            cv2.putText(frame, ("target lost"), (20, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,(0, 0, 255), 2)
            roi = frame[0:100,0:100]

        sd_mask= sd.ellipse_detect(roi)
        # sd_mask = sd.cr_otsu(roi)
        # sd_mask= sd.crcb_range_sceening(roi)
        # sd_mask = sd.hsv_detect(roi)

        _, contours, hierarchy = cv2.findContours(sd_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(sd_mask, contours, -1, (255, 255, 255), -1)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        sd_mask = cv2.dilate(sd_mask, kernel, iterations=1)

        hand=cv2.bitwise_and(roi, roi, mask=sd_mask)#有时间看看
        cv2.putText(frame, ("interval:" + str(round(freq_aver,3))), (20, 30), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2,
                    (0, 0, 255),2)
        hand = cv2.resize(hand,(164,164))

        cv2.imshow("frame", frame)
        cv2.imshow("mask", sd_mask)
        cv2.imshow("hand", hand)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("i"):
            print "aa"
    else:
        print "播放结束"
        cv2.destroyAllWindows()
        camera.release()
        break
    end = time.time()
    freq.insert(0,end-begin)
    if len(freq)>9:
        freq_aver= sum(freq)/10
        freq.pop()
        print "耗时：",freq_aver



































