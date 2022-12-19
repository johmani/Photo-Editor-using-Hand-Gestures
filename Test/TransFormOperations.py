import cv2
import numpy as np

import cv2
import numpy as np


class TransForm:

    def Translate(image,dx,dy):
        M = np.float32([[1, 0, dx], [0, 1, dy]])
        result = cv2.warpAffine(image, M, (image.shape[0], image.shape[1]))
        return result

    def Rotate(image):
        result = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        return result

    def Scale(image,w,h):
        result = cv2.resize(image, (w, h))
        return result



# Test:
# img= cv2.imread('../Assets/R.png')
# img = TransForm.Translate(img,90,89)
# cv2.imshow('img',img)
# cv2.waitKey(0)


