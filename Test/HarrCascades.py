# Importing all required packages
import cv2
import numpy as np
import matplotlib.pyplot as plt



face_cascade = cv2.CascadeClassifier('../Assets/haarcascade_frontalface_default.xml')


def DeletFace(img):
    deletedFaceImage = img.copy()
    face_rect = face_cascade.detectMultiScale(deletedFaceImage,scaleFactor=1.2,minNeighbors=5)
    for (x, y, w, h) in face_rect:
        cv2.rectangle(deletedFaceImage, (x, y),(x + w, y + h), (0,0,0), -1)
    return deletedFaceImage


cap = cv2.VideoCapture('http://192.168.43.1:8080/video')

while (True):
    ret, frame = cap.read()
    # frame = cv2.flip(frame, 1)
    face = DeletFace(frame)
    cv2.imshow("Harr",face)

    k = cv2.waitKey(1)

cv2.destroyAllWindows()
cap.release()