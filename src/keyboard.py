import math
import numpy as np
from numpy.linalg import norm
import cv2

class Key(object):
    def __init__(self, key, top_left, width, height):
        self.key = key
        self.top_left = np.array(top_left).ravel()
        self.center = self.top_left + [width/2, height/2]
        self.width = width
        self.height = height
        self.rad = math.sqrt(width**2 + height**2)/2

    def relative_dist(self, point):
        return norm(point - self.center)/self.rad

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
        self.corners = sort_clockwise(corners)
        self.real_corners = sort_clockwise(np.array([(6,24),(130,24),(130,64),(6,64)]))
        self._init_homog()
        self.size_inch = (136,88)
        self.size_pix = None
        dx = 12
        dy = 12
        rowdx = 6
        self.keys = [
                     Key('q', (9+0*dx, 27), 10, 10),
                     Key('w', (9+1*dx, 27), 10, 10),
                     Key('e', (9+2*dx, 27), 10, 10),
                     Key('r', (9+3*dx, 27), 10, 10),
                     Key('t', (9+4*dx, 27), 10, 10),
                     Key('y', (9+5*dx, 27), 10, 10),
                     Key('u', (9+6*dx, 27), 10, 10),
                     Key('i', (9+7*dx, 27), 10, 10),
                     Key('o', (9+8*dx, 27), 10, 10),
                     Key('p', (9+9*dx, 27), 10, 10),
                     Key('a', (9+rowdx+0*dx, 27+dy), 10, 10),
                     Key('s', (9+rowdx+1*dx, 27+dy), 10, 10),
                     Key('d', (9+rowdx+2*dx, 27+dy), 10, 10),
                     Key('f', (9+rowdx+3*dx, 27+dy), 10, 10),
                     Key('g', (9+rowdx+4*dx, 27+dy), 10, 10),
                     Key('h', (9+rowdx+5*dx, 27+dy), 10, 10),
                     Key('j', (9+rowdx+6*dx, 27+dy), 10, 10),
                     Key('k', (9+rowdx+7*dx, 27+dy), 10, 10),
                     Key('l', (9+rowdx+8*dx, 27+dy), 10, 10),
                     Key('z', (9+2*rowdx+0*dx, 27+2*dy), 10, 10),
                     Key('x', (9+2*rowdx+1*dx, 27+2*dy), 10, 10),
                     Key('c', (9+2*rowdx+2*dx, 27+2*dy), 10, 10),
                     Key('v', (9+2*rowdx+3*dx, 27+2*dy), 10, 10),
                     Key('b', (9+2*rowdx+4*dx, 27+2*dy), 10, 10),
                     Key('n', (9+2*rowdx+5*dx, 27+2*dy), 10, 10),
                     Key('m', (9+2*rowdx+6*dx, 27+2*dy), 10, 10)
                     ]

    def inch2pix(self, point):
        if self.size_pix is None:
            self._load_img()
        rat = [self.size_pix[i]/float(self.size_inch[i]) for i in range(2)]
        return [point[i]*rat[i] for i in range(2)]

    def _load_img(self):
        PrintedKeyboard.img = cv2.imread('Keyboard.png')
        h,w = PrintedKeyboard.img.shape[:2]
        self.size_pix = (w,h)

    def key_center(self, key):
        for k in self.keys:
            if k.key == key:
                return k.center
        return None

    def image(self):
        if PrintedKeyboard.img is None:
            self._load_img()
        return PrintedKeyboard.img.copy()
