import threading
import tkinter as tk
from tkinter import ttk

from ImageEditor.Functionality import Functionality
from editBar import EditBar
from imageViewer import ImageViewer
from pynput.mouse import Controller
from HandGestures.Detection import *
from HandGestures.Contour import *


class Main(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self.filename = ""
        self.original_image = None
        self.processed_image = None
        self.is_image_selected = False
        self.is_draw_state = False
        self.drawColor = "red"
        self.thickness = 2

        self.title("Image Editor")

        self.editbar = EditBar(master=self)
        separator1 = ttk.Separator(master=self, orient=tk.HORIZONTAL)
        self.image_viewer = ImageViewer(master=self)

        self.editbar.pack(pady=10)
        separator1.pack(fill=tk.X, padx=20, pady=5)
        self.image_viewer.pack(fill=tk.BOTH, padx=20, pady=10, expand=1)



        self.cap = cv.VideoCapture(0)

        _, firstFrame = self.cap.read()
        cv.rectangle(firstFrame, (380, 0), (635, 475), (0, 255, 0), 1)
        roi2 = firstFrame[0:475, 380:635]
        r, h, c, w = 0, 240, 0, 640
        self.track_window = (c, r, w, h)
        [self.hist] = histogram(roi2, self.cap, r, h, c, w)
        self.term_crit = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1)

        self.bgCaptured = False
        cv.namedWindow("Value")
        cv.resizeWindow("Value", 300, 25)
        cv.createTrackbar("Value", "Value", 0, 255, nothing)
        cv.setTrackbarPos("Value", "Value", 20)

        self.mouse = Controller()
        self.count = 0
        self.ex = 0

        self.trigger = False
        x = threading.Thread(target = self.MainLoop)
        x.start()

    def MainLoop(self):
        while True:
            ret, frame = self.cap.read()
            frame = cv.flip(frame, 1)
            cv.imshow("Live", frame)
            k = cv.waitKey(1)
            cv.rectangle(frame, (380, 0), (635, 475), (0, 255, 0), 1)
            roi3 = frame[0:475, 380:635]

            hsv = cv.cvtColor(roi3, cv.COLOR_BGR2HSV)
            dst = cv.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
            ret, self.track_window = cv.CamShift(dst, self.track_window, self.term_crit)
            pts = cv.boxPoints(ret)
            pts = np.int0(pts)

            if self.bgCaptured is True:
                mask = subtractBg(roi3, bgCap)

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

                if self.trigger is True:
                    self.recognizeGestures(res,num_def,self.count,farthest_point)






                cv.imshow("Live", frame)
                cv.imshow("Result", res)
                # cv.imshow("Threshold", rThresh)
                # cv.imshow("Mask", mask)

            k = cv.waitKey(1)
            if k & 0xFF == 27:
                break
            elif k == ord("c"):
                bgCap = cv.createBackgroundSubtractorMOG2(0, 50)
                print("C")
                self.bgCaptured = True
            elif k == ord("a"):
                print("A")
                self.trigger = True

        cv.destroyAllWindows()
        self.cap.release()




    def recognizeGestures(self,frame, num_def, count, farthest_point):
        try:
            if num_def == 1:
                cv.putText(frame, "2", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
                if count == 0:
                    self.processed_image = Functionality.Translate(self.processed_image, 10, 0)
                    count = 1

            elif num_def == 2:
                cv.putText(frame, "3", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
                if count == 0:
                    self.processed_image = Functionality.Rotate(self.processed_image)
                    count = 1

            elif num_def == 3:
                cv.putText(frame, "4", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
                if count == 0:
                    self.processed_image = Functionality.Scale(self.processed_image, 0.8, 0.8)

                    count = 1

            elif num_def == 4:
                cv.putText(frame, "5", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
                if count == 0:
                    # TODO
                    count = 1

            else:
                cv.putText(frame, "1", (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3, cv.LINE_AA)
                # TODO
                count = 0

            self.image_viewer.master.image_viewer.show_image()
        except:
            print("You moved the hand too fast or take it out of range of vision of the camera")





