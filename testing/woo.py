import numpy as np
import cv2
import sys

cap = cv2.VideoCapture('test.mp4')
i = 0
j=0
while(cap.isOpened())
    try:
        ret, frame = cap.read()
        if i%45 == 0:
            f = resized_image = cv2.resize(frame, (1000, 500))
            cv2.imwrite('image'+j.__str__()+'.png',f)
            j=j+1
            print frame.size
        i= i+1
    except:
        cap.release()
        sys.exit(0)
cap.release()
sys.exit(0)
