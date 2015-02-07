import math
import numpy as np
from numpy.linalg import norm
import cv2

from keyboard_layout import PrintedKeyboardLayout

class WeightedKey(object):
    def __init__(self, key, weight):
        self.key = key
        self.weight = weight

def sort_clockwise(points):
    # p1 ----- p2
    # |         |
    # |         |
    # p4 ----- p3
    if len(points) != 4:
        return points
    by_x  = sorted(points, key=lambda p: p[0])
    left  = sorted(by_x[0:2], key=lambda p: p[1])
    right = sorted(by_x[2:4], key=lambda p: p[1])
    return [left[0], right[0], right[1], left[1]]

class Keyboard(object):
    def _init_homog(self):
        if len(self.corners) != 4:
            return
        src = np.float32(self.corners).reshape(-1, 1, 2)
        dst = np.float32(self.real_corners).reshape(-1, 1, 2)
        self.H, _mask = cv2.findHomography(src, dst)

    def point_in_keyboard_coord(self, point):
        ''' Returns the coordinates of the point in the keyboard image '''
        if len(self.corners) != 4:
            return point
        pt = np.float32(point).reshape(-1, 1, 2)
        return cv2.perspectiveTransform(pt, self.H).ravel()

    def weighted_keys(self, fixation):
        wk = []
        for key in self.keys:
            dist = key.relative_dist(fixation)
            if dist < 2:
                wk.append(WeightedKey(key.key, dist))
        eps = 1e-10 # To avoid division by 0
        total = np.sum([1/(k.weight+eps) for k in wk])
        return [WeightedKey(k.key, 1/((k.weight+eps)*total)) for k in wk]

class PrintedKeyboard(Keyboard):
    img = None

    def __init__(self, corners=[]):
        layout = PrintedKeyboardLayout()
        self.corners = sort_clockwise(corners)
        self.real_corners = sort_clockwise(np.array(layout.corners))
        self._init_homog()
        self.size_inch = (136,88)
        self.size_pix = None
        self.keys = layout.keys

    def inch2pix(self, point):
        if self.size_pix is None:
            self._load_img()
        rat = [self.size_pix[i]/float(self.size_inch[i]) for i in range(2)]
        return [point[i]*rat[i] for i in range(2)]

    def _load_img(self):
        PrintedKeyboard.img = cv2.imread('Keyboard.png')
        h,w = PrintedKeyboard.img.shape[:2]
        self.size_pix = (w,h)

    def image(self):
        if PrintedKeyboard.img is None:
            self._load_img()
        return PrintedKeyboard.img.copy()
