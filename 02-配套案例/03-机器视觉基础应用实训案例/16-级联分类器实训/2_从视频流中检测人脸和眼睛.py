#!/usr/bin env python3
# -*- coding:UTF8 -*-

"""
        
"""

import cv2 as cv

face_cascade = cv.CascadeClassifier('./haarcascade/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('./haarcascade/haarcascade_eye.xml')

cap = cv.VideoCapture(0)

while cap.isOpened():
    frame = cap.read()[1]
    frame = cv.resize(frame, None, fx = .5, fy = .5)
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    faces_rects = face_cascade.detectMultiScale(frame_gray, scaleFactor = 1.2, minNeighbors = 5)
    for x, y, w, h in faces_rects:
        frame = cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = frame_gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for ex, ey, ew, eh in eyes:
            cv.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    cv.imshow('frame_face', frame)
    k = cv.waitKey(24) & 0Xff
    if chr(k) == 'q':
        break
cv.destroyAllWindows()
