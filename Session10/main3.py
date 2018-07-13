import cv2
from Session10.webcam import webcam
import numpy as np


# cap = cv2.VideoCapture(0)
list_webcam = []
for i in range(80):
    a = webcam(i).update()
    list_webcam.append(a)



#
# while True:
#     ret, frame = cap.read()
#     cv2.imshow("video1", frame)
#     k = cv2.waitKey(30)
#
#     if k == 27:
#         cap.release()
#         break