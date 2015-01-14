import cv2
import numpy as np

from keyboard import PrintedKeyboard

class ManualKeyboardDetector(object):
    def __init__(self):
        self.prev_frame = None
        self.win_name = 'Select corners'
        self.points = []
        self.lk_params = dict( winSize  = (90, 90),
                               maxLevel = 3,
                               criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 20, 0.03))
        self.rad = 5

    def detect(self, frame):
        self.img = frame
        keyboard = None
        if self.prev_frame is None:
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
                    return PrintedKeyboard([])
            cv2.destroyWindow(self.win_name)
            self.points = np.array(self.points, np.float32)
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