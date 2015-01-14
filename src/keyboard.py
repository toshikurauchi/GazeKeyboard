import math
import numpy as np
from numpy.linalg import norm
import cv2

class Key(object):
    def __init__(self, key, center, width, height):
        self.key = key
        self.center = np.array(center).ravel()
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
    img = None

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

    def image(self):
        if Keyboard.img is None:
            Keyboard.img = cv2.imread('Keyboard.png')
        return Keyboard.img.copy()

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
    def __init__(self, corners=[]):
        self.corners = sort_clockwise(corners)
        self.real_corners = sort_clockwise(np.array([(110,450),(2440,450),(2440,1200),(110,1200)]))
        self._init_homog()
        dx = 224
        dy = 224
        rowdx = 112
        self.keys = [
                     Key('q', (260+0*dx, 596), 185, 185),
                     Key('w', (260+1*dx, 596), 185, 185),
                     Key('e', (260+2*dx, 596), 185, 185),
                     Key('r', (260+3*dx, 596), 185, 185),
                     Key('t', (260+4*dx, 596), 185, 185),
                     Key('y', (260+5*dx, 596), 185, 185),
                     Key('u', (260+6*dx, 596), 185, 185),
                     Key('i', (260+7*dx, 596), 185, 185),
                     Key('o', (260+8*dx, 596), 185, 185),
                     Key('p', (260+9*dx, 596), 185, 185),
                     Key('a', (260+rowdx+0*dx, 596+dy), 185, 185),
                     Key('s', (260+rowdx+1*dx, 596+dy), 185, 185),
                     Key('d', (260+rowdx+2*dx, 596+dy), 185, 185),
                     Key('f', (260+rowdx+3*dx, 596+dy), 185, 185),
                     Key('g', (260+rowdx+4*dx, 596+dy), 185, 185),
                     Key('h', (260+rowdx+5*dx, 596+dy), 185, 185),
                     Key('j', (260+rowdx+6*dx, 596+dy), 185, 185),
                     Key('k', (260+rowdx+7*dx, 596+dy), 185, 185),
                     Key('l', (260+rowdx+8*dx, 596+dy), 185, 185),
                     Key('z', (260+2*rowdx+0*dx, 596+2*dy), 185, 185),
                     Key('x', (260+2*rowdx+1*dx, 596+2*dy), 185, 185),
                     Key('c', (260+2*rowdx+2*dx, 596+2*dy), 185, 185),
                     Key('v', (260+2*rowdx+3*dx, 596+2*dy), 185, 185),
                     Key('b', (260+2*rowdx+4*dx, 596+2*dy), 185, 185),
                     Key('n', (260+2*rowdx+5*dx, 596+2*dy), 185, 185),
                     Key('m', (260+2*rowdx+6*dx, 596+2*dy), 185, 185)
                     ]
