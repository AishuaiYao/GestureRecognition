# -*- coding:utf-8 -*-
import cv2
import numpy as np
import motiondetection as md

def absdiff(image_1, image_2, sThre):
    gray_image_1 = cv2.cvtColor(image_1, cv2.COLOR_BGR2GRAY)  # 灰度化
    gray_image_1 = cv2.GaussianBlur(gray_image_1, (3, 3), 0)  # 高斯滤波
    gray_image_2 = cv2.cvtColor(image_2, cv2.COLOR_BGR2GRAY)
    gray_image_2 = cv2.GaussianBlur(gray_image_2, (3, 3), 0)
    d_frame = cv2.absdiff(gray_image_1, gray_image_2)
    ret, d_frame = cv2.threshold(d_frame, sThre, 255, cv2.THRESH_BINARY)
    return d_frame


def backgrounddifference(frame,fgbg):
    fgmask = fgbg.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgmask = cv2.erode(fgmask, kernel, iterations=1)
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    fgmask = cv2.dilate(fgmask,kernel, iterations=10)
    _, contours, hierarchy = cv2.findContours(fgmask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    ROI=None
    if contours is not None:
        for c in contours:
            if cv2.contourArea(c) <2999:
                continue
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.putText(frame, "ROIsize:"+str(cv2.contourArea(c)),(20, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255),2)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            ROI=frame[y:y + h, x:x + w]

    return fgmask,ROI


# def location():
#     md_mask = md.absdiff(frame, last_frame, sThre)
#     last_frame = frame.copy()
#
#     md_mask = cv2.erode(md_mask, None, iterations=1)
#     md_mask = cv2.dilate(md_mask, None, iterations=2)
#     contours, hierarchy = cv2.findContours(md_mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     # ctrl+鼠标点击看函数定义
#     newcontours = []
#     if contours is not None:
#         for c in contours:
#             if cv2.contourArea(c) < 300:
#                 continue
#             newcontours.append(c[0])
            # M = cv2.moments(c)
            # cx = int(M['m10'] / M['m00'])
            # cy = int(M['m01'] / M['m00'])
            # centroid=(cx,cy)
            # distance=getDistance(centroid,last_centroid)
            # print "质心距离：",distance
            # last_centroid = centroid
            # if(distance>30) and (distance<50):
            # cv2.putText(frame,"*",(cx,cy), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1,(0,0,255),2,)
            # hull_cv = cv2.convexHull(newcontours)
            # cv2.drawContours(frame, [hull_cv], 0, (0, 0, 255), 2)
#         if newcontours:
#             newcontours = np.array(newcontours)
#             #                 print "新多边形的点：", newcontours
#             #                 print "n的类型：", type(newcontours)
#             #                 hull_cv = cv2.convexHull(newcontours)
#             #                 cv2.drawContours(frame, [hull_cv], 0, (0, 0, 255), 2)
#             (x, y, w, h) = cv2.boundingRect(newcontours)
#             #                 cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),2)
#             seperate = frame[y:(y + h * 1), x:(x + w * 1)]
#             fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel, iterations=1)  # 形态学开运算


last_centroid=(0,0)
def getDistance(pointa,pointb ):
    distance = np.square((pointa[0] - pointb[0])) + np.square((pointa[1] - pointb[1]))
    distance = np.sqrt(distance)
    return distance

































