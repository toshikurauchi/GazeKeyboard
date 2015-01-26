import cv2
import os
import numpy as np
import csv

from keyboard import PrintedKeyboard

class ManualKeyboardDetector(object):
    def __init__(self, corners_path, redetect=0):
        self.prev_frame = None
        self.win_name = 'Select corners'
        self.points = []
        self.lk_params = dict( winSize  = (90, 90),
                               maxLevel = 3,
                               criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.03))
        self.rad = 5
        self.frame_count = 0
        self.frame_id = None
        self.corners_path = corners_path
        if os.path.isfile(corners_path) and not redetect:
            with open(corners_path, 'rb') as csvfile:
                spamreader = csv.reader(csvfile, delimiter=',')
                for row in spamreader:
                    if self.frame_id is None:
                        self.frame_id = int(row[0])
                    else:
                        self.points.append([float(p) for p in row])
                self.points = np.array(self.points, np.float32)

    def detect(self, frame):
        self.frame_count += 1
        self.img = frame
        keyboard = None
        if self.prev_frame is None:
            if self.frame_id is None:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                self.corners = cv2.goodFeaturesToTrack(gray, 1000, 0.01, 10)
                self.corners = np.int0(self.corners)
                col = (0, 0, 255)
                for c in self.corners:
                    x,y = c.ravel()
                    cv2.circle(self.img, (x,y), self.rad, col, -1)

                cv2.imshow(self.win_name, self.img)
                cv2.setMouseCallback(self.win_name, self.on_mouse)

                while len(self.points) < 4:
                    key = cv2.waitKey(1)
                    if key == 27:
                        return None
                    if key == 10 or key == 13:
                        self.points = []
                        return PrintedKeyboard()
                with open(self.corners_path, 'wb') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=',')
                    spamwriter.writerow([self.frame_count])
                    for p in self.points:
                        spamwriter.writerow(p)
                cv2.destroyWindow(self.win_name)

                self.points = np.array(self.points, np.float32)
            elif self.frame_id > self.frame_count:
                return PrintedKeyboard()
        else:
            self.points, _s, _e = cv2.calcOpticalFlowPyrLK(self.prev_frame, frame, self.points, minEigThreshold=0.005, **self.lk_params)
        keyboard = PrintedKeyboard(self.points)
        self.prev_frame = frame
        return keyboard

    def on_mouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            idx = np.argmin([(x-c[0,0])**2 + (y-c[0,1])**2 for c in self.corners])
            px,py = self.corners[idx].ravel()
            self.points.append((px,py))
            col = (0, 255, 0)
            for p in self.points:
                cv2.circle(self.img, p, self.rad, col, -1)
            cv2.imshow(self.win_name, self.img)