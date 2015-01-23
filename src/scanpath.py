import numpy as np
import cv2

from gaze_data import Fixation
from keyboard import PrintedKeyboard
from util import load_or_detect_fixations

class ScanpathPlotter(object):
    def __init__(self, folder, redetect=0):
        self.max_fix_rad = 50
        self.fix_color   = (0, 0, 255)
        self.sac_color   = (0, 255, 0)

        self.fixations = load_or_detect_fixations(folder, redetect)

    def plot(self):
        keyboard = PrintedKeyboard()
        for f in self.fixations:
            f.pos = keyboard.inch2pix(f.pos)
        max_duration = np.max([f.duration for f in self.fixations])
        kb_img = keyboard.image()
        # Draw scanpat
        for i in range(len(self.fixations)-1):
            pos1 = tuple(np.int0(self.fixations[i].pos))
            pos2 = tuple(np.int0(self.fixations[i+1].pos))
            cv2.line(kb_img, pos1, pos2, self.sac_color, 5)
        for f in self.fixations:
            rad = int(self.max_fix_rad * float(f.duration) / max_duration)
            cv2.circle(kb_img, tuple(np.int0(f.pos)), rad, self.fix_color, -1)
        # Resize image to show
        h, w = kb_img.shape[0:2]
        new_w = 1000
        kb_img = cv2.resize(kb_img, (new_w, new_w*h/w))
        cv2.imshow('Player', kb_img)
        while cv2.waitKey(0) != 27:
            pass
        cv2.destroyAllWindows()

if __name__=='__main__':
    import sys

    redetect = 0
    if len(sys.argv) < 2:
        print "USAGE: {p} TRIAL_FOLDER".format(p=sys.argv[0])
        sys.exit()
    if len(sys.argv) > 2:
        redetect = int(sys.argv[2])

    folder = sys.argv[1]
    ScanpathPlotter(folder, redetect).plot()
