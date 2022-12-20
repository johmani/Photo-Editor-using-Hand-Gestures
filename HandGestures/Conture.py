import cv2 as cv
import numpy as np
import math



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