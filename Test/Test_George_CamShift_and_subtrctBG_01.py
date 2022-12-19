import cv2 as cv
import numpy as np
import os
import math
import time
from pynput.mouse import Button, Controller


def nothing(x):
    pass


def histogram(firstFrame, r, h, c, w):
    # roi = firstFrame[r:r+h, c:c+w]
    hsv_roi = cv.cvtColor(firstFrame, cv.COLOR_BGR2HSV)
    hl, hu, sl, su, vl, vu = setMask()
    low = np.array([hl, sl, vl])
    up = np.array([hu, su, vu])
    mask = cv.inRange(hsv_roi, low, up)
    hist = cv.calcHist([hsv_roi], [0], mask, [180], [0, 180])
    cv.normalize(hist, hist, 0, 255, cv.NORM_MINMAX)

    return [hist]


def setMask():
    cv.namedWindow("Settings")
    cv.resizeWindow("Settings", 640, 250)

    cv.createTrackbar("H Low", "Settings", 0, 180, nothing)
    cv.createTrackbar("H Up", "Settings", 0, 180, nothing)
    cv.createTrackbar("S Low", "Settings", 0, 255, nothing)
    cv.createTrackbar("S Up", "Settings", 0, 255, nothing)
    cv.createTrackbar("V Low", "Settings", 0, 255, nothing)
    cv.createTrackbar("V Up", "Settings", 0, 255, nothing)

    cv.setTrackbarPos("H Low", "Settings", 0)
    cv.setTrackbarPos("H Up", "Settings", 180)
    cv.setTrackbarPos("S Low", "Settings", 0)
    cv.setTrackbarPos("S Up", "Settings", 255)
    cv.setTrackbarPos("V Low", "Settings", 0)
    cv.setTrackbarPos("V Up", "Settings", 255)

    while (1):
        _, frame = cap.read()
        frame = cv.flip(frame, 1)
        cv.rectangle(frame, (380, 0), (635, 475), (0, 255, 0), 1)
        roi = frame[0:475, 380:635]
        hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

        hl = cv.getTrackbarPos("H Low", "Settings")
        hu = cv.getTrackbarPos("H Up", "Settings")
        sl = cv.getTrackbarPos("S Low", "Settings")
        su = cv.getTrackbarPos("S Up", "Settings")
        vl = cv.getTrackbarPos("V Low", "Settings")
        vu = cv.getTrackbarPos("V Up", "Settings")

        low = np.array([hl, sl, vl])
        up = np.array([hu, su, vu])

        mask = cv.inRange(hsv, low, up)
        ker = np.ones((5, 5), np.uint8)

        mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, ker)
        mask = cv.dilate(mask, ker, iterations=1)
        mask = cv.morphologyEx(mask, cv.MORPH_OPEN, ker)
        mask = cv.medianBlur(mask, 15)
        res = cv.bitwise_and(roi, roi, mask=mask)

        cv.imshow("Original", frame)
        cv.imshow("Filter", res)

        k = cv.waitKey(1)
        if k & 0xFF == ord("s"):
            break

    cv.destroyAllWindows()

    return hl, hu, sl, su, vl, vu


def subtractBg(frame):
    fgMask = bgCap.apply(frame, learningRate=0)
    ker = np.ones((3, 3), np.uint8)
    fgMask = cv.erode(fgMask, ker, iterations=1)
    res = cv.bitwise_and(frame, frame, mask=fgMask)

    return res


def findMaxContour(rThresh):
    con, _ = cv.findContours(rThresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    max_i = 0
    max_area = 0
    for i in range(len(con)):
        hand = con[i]
        area_hand = cv.contourArea(hand)
        if area_hand > max_area:
            max_area = area_hand
            max_i = i
    try:
        max_con = con[max_i]
    except:
        con = [0]
        max_con = con[0]

    return con, max_con


def findFingers(res, max_con):
    try:
        hull = cv.convexHull(max_con, returnPoints=False)
        defects = cv.convexityDefects(max_con, hull)
        if defects is None:
            defects = [0]
            num_def = 0
        else:
            num_def = 0
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(max_con[s][0])
                end = tuple(max_con[e][0])
                far = tuple(max_con[f][0])

                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                d = (2 * ar) / a

                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                if angle <= 90 and d > 30:
                    num_def += 1
                    cv.circle(res, far, 3, (255, 0, 0), -1)

                cv.line(res, start, end, (0, 0, 255), 2)

        return defects, num_def

    except:
        defects = [0]
        num_def = 0

        return defects, num_def


def centroid(max_con):
    moment = cv.moments(max_con)
    if moment is None:
        cx = 0
        cy = 0

        return cx, cy

    else:
        cx = 0
        cy = 0
        if moment["m00"] != 0:
            cx = int(moment["m10"] / moment["m00"])
            cy = int(moment["m01"] / moment["m00"])

        return cx, cy


def findFarPoint(res, cx, cy, defects, max_con):
    try:
        s = defects[:, 0][:, 0]

        x = np.array(max_con[s][:, 0][:, 0], dtype=np.float)
        y = np.array(max_con[s][:, 0][:, 1], dtype=np.float)

        xp = cv.pow(cv.subtract(x, cx), 2)
        yp = cv.pow(cv.subtract(y, cy), 2)

        dist = cv.sqrt(cv.add(xp, yp))
        dist_max_i = np.argmax(dist)

        if dist_max_i < len(s):
            farthest_defect = s[dist_max_i]
            farthest_point = tuple(max_con[farthest_defect][0])

        cv.line(res, (cx, cy), farthest_point, (0, 255, 255), 2)

        return farthest_point

    except:
        farthest_point = 0

        return farthest_point


def recognizeGestures(frame, num_def, count, farthest_point, imge):
    try:
        if num_def == 1:
            cv.putText(frame, "2", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
            if count == 0:
                cv.destroyWindow('My Zen Garden')
                cv.destroyWindow('dst')
                cv.destroyWindow('scale_image')
                # cv.destroyWindow ('image_original')
                cv.destroyWindow('rotate_image')
                img = cv.imread('Lenna.jpg')
                cv.imshow('image_original', img)
                height, width = img.shape[:2]
                quarter_height, quarter_width = height / 4, width / 4
                T = np.float32([[1, 0, quarter_width], [0, 1, quarter_height]])
                img_translation = cv.warpAffine(img, T, (width, height))
                cv.imshow('Translation', img_translation)

                # cv.waitKey()

                # print("2")
                # mouse.position=(1293,19)
                # mouse.click(Button.left)
                # mouse.release(Button.left)
                # mouse.position = (341, 82)
                # mouse.press(Button.left)
                # mouse.release(Button.left)
                mouse.position = farthest_point
                count = 1

        elif num_def == 2:
            cv.putText(frame, "3", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
            if count == 0:
                cv.destroyWindow('My Zen Garden')
                cv.destroyWindow('dst')
                cv.destroyWindow('scale_image')
                cv.destroyWindow('image_original')
                cv.destroyWindow('Translation')
                img = cv.imread('Lenna.jpg')
                image = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
                cv.imshow('rotate_image', image)
                # mouse.release(Button.left)
                #  mouse.position = (254, 106)
                #  mouse.press(Button.left)
                #  mouse.release(Button.left)
                mouse.position = farthest_point
                count = 1

        elif num_def == 3:
            cv.putText(frame, "4", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
            if count == 0:
                cv.destroyWindow('My Zen Garden')
                cv.destroyWindow('dst')
                cv.destroyWindow('rotate_image')
                cv.destroyWindow('image_original')
                cv.destroyWindow('Translation')
                img = cv.imread('Lenna.jpg')
                half = cv.resize(img, (0, 0), fx=0.1, fy=0.1)
                cv.imshow('scale_image', half)
                #  mouse.release(Button.left)
                #  mouse.position = (837, 69)
                #  mouse.press(Button.left)
                #  mouse.release(Button.left)
                # mouse.position = farthest_point
                count = 1

        elif num_def == 4:
            cv.putText(frame, "5", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
            if count == 0:
                cv.destroyWindow('scale_image')
                cv.destroyWindow('dst')
                cv.destroyWindow('rotate_image')
                cv.destroyWindow('image_original')
                cv.destroyWindow('Translation')
                img = cv.imread('Lenna.jpg')
                rows, cols, ch = img.shape
                pts1 = np.float32(
                    [[cols * .25, rows * .95],
                     [cols * .90, rows * .95],
                     [cols * .10, 0],
                     [cols, 0]]
                )
                pts2 = np.float32(
                    [[cols * 0.1, rows],
                     [cols, rows],
                     [0, 0],
                     [cols, 0]]
                )
                M = cv.getPerspectiveTransform(pts1, pts2)
                dst = cv.warpPerspective(img, M, (cols, rows))
                cv.imshow('My Zen Garden', dst)
                #   mouse.release(Button.left)
                #   mouse.position = (772, 69)
                #   mouse.press(Button.left)
                #   mouse.release(Button.left)
                #   mouse.position = farthest_point
                count = 1

        else:
            cv.putText(frame, "1", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
            cv.destroyWindow('scale_image')
            cv.destroyWindow('My Zen Garden')
            cv.destroyWindow('rotate_image')
            cv.destroyWindow('image_original')
            cv.destroyWindow('Translation')
            img = cv.imread('Lenna.jpg')
            pts1 = np.float32([[56, 65], [368, 52], [28, 387], [389, 390]])
            pts2 = np.float32([[0, 0], [300, 0], [0, 300], [300, 300]])
            M = cv.getPerspectiveTransform(pts1, pts2)
            dst = cv.warpPerspective(img, M, (300, 300))
            cv.imshow('dst', dst);

            # mouse.position = farthest_point
            # mouse.press(Button.left)
            count = 0

    except:
        print("You moved the hand too fast or take it out of range of vision of the camera")


cap = cv.VideoCapture('http://192.168.43.1:8080/video')

_, firstFrame = cap.read()
cv.rectangle(firstFrame, (380, 0), (635, 475), (0, 255, 0), 1)
roi2 = firstFrame[0:475, 380:635]
r, h, c, w = 0, 240, 0, 640
track_window = (c, r, w, h)
[hist] = histogram(roi2, r, h, c, w)
term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

bgCaptured = False
cv.namedWindow("Value")
cv.resizeWindow("Value", 300, 25)
cv.createTrackbar("Value", "Value", 0, 255, nothing)
cv.setTrackbarPos("Value", "Value", 20)

mouse = Controller()
count = 0
ex = 0

trigger = False
# os.startfile("D:\Program_George\phone_me\Tenorshare\Tenorshare Phone Mirror\PhoneMirror.exe")
img = cv.imread(r'C:\Users\mohamd\Desktop\Photo-Editorusing-Hand-Gestures\Assets\DNA1.png')
# cv.imshow('image_original',img)

while (1):
    # start = time.time()
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)

    cv.rectangle(frame, (380, 0), (635, 475), (0, 255, 0), 1)
    roi3 = frame[0:475, 380:635]

    hsv = cv.cvtColor(roi3, cv.COLOR_BGR2HSV)
    dst = cv.calcBackProject([hsv], [0], hist, [0, 180], 1)
    ret, track_window = cv.CamShift(dst, track_window, term_crit)
    pts = cv.boxPoints(ret)
    pts = np.int0(pts)

    if bgCaptured is True:
        mask = subtractBg(roi3)

        vThresh = cv.getTrackbarPos("Value", "Value")

        ker = np.ones((5, 5), np.uint8)

        img = np.zeros(roi3.shape, np.uint8)
        chanCount = mask.shape[2]
        ignoreColor = (255,) * chanCount
        cv.fillConvexPoly(img, pts, ignoreColor)
        res = cv.bitwise_and(mask, img)

        resMask = cv.dilate(res, ker, iterations=1)
        resMask = cv.morphologyEx(resMask, cv.MORPH_OPEN, ker)
        resMask = cv.medianBlur(resMask, 15)
        resMask = cv.cvtColor(resMask, cv.COLOR_BGR2GRAY)
        _, rThresh = cv.threshold(resMask, vThresh, 255, cv.THRESH_BINARY)

        con, max_con = findMaxContour(rThresh)

        defects, num_def = findFingers(res, max_con)

        cx, cy = centroid(max_con)
        if np.all(con[0] > 0):
            cv.circle(res, (cx, cy), 5, (0, 255, 0), 2)
        else:
            pass

        farthest_point = findFarPoint(res, cx, cy, defects, max_con)

        if trigger is True:
            recognizeGestures(roi3, num_def, count, farthest_point, img)

        cv.imshow("Live", frame)
        cv.imshow("Result", res)
        cv.imshow("Threshold", rThresh)
        cv.imshow("Mask", mask)
        # cv.imshow("test", )
        # end = time.time()
        # seconds = end - start
        # print("Time taken : {0} seconds".format(seconds))

    k = cv.waitKey(1)
    if k & 0xFF == 27:
        break
    elif k == ord("c"):
        bgCap = cv.createBackgroundSubtractorMOG2(0, 50)
        bgCaptured = True
    elif k == ord("a"):
        trigger = True

cv.destroyAllWindows()
# os.system("TASKKILL /F /IM PhoneMirror.exe")
cap.release()