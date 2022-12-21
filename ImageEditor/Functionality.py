import cv2
import numpy as np


class Functionality:

    def Translate(image, dx, dy):
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        result = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
        return result

    def Rotate(image):
        result = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return result

    def Scale(image,sx,sy):
        result = cv2.resize(image, (0, 0), fx=sx, fy=sy)
        return result



