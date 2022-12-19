import cv2

def DeletFace(img):
    face_cascade = cv2.CascadeClassifier('../Assets/haarcascade_frontalface_default.xml')
    deletedFaceImage = img.copy()
    face_rect = face_cascade.detectMultiScale(deletedFaceImage,scaleFactor=1.2,minNeighbors=5)
    for (x, y, w, h) in face_rect:
        cv2.rectangle(deletedFaceImage, (x, y),(x + w, y + h), (0,0,0), -1)
    return deletedFaceImage
