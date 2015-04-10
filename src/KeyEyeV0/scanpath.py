import numpy as np
import os
import cv2

from gaze_data import Fixation
from keyboard import PrintedKeyboard
from util import load_or_detect_fixations

class ScanpathPlotter(object):
    def __init__(self, folder, redetect=False, unfiltered=False):
        self.max_fix_rad = 50
        self.fix_color   = (0, 0, 255)
        self.sac_color   = (0, 255, 0)

        fixations = load_or_detect_fixations(folder, redetect)
        if unfiltered:
            gaze = np.load(os.path.join(folder, 'keyboard_gaze.npy'))[:,0:1]
            self.data = [[g[0][0], g[0][1], 1] for g in gaze]
            self.max_fix_rad = 5
        else:
            max_duration = np.max([f.duration for f in fixations])
            self.data = [[f.pos[0], f.pos[1], float(f.duration)/max_duration] for f in fixations]

    def plot(self):
        keyboard = PrintedKeyboard()
        for d in self.data:
            d[:2] = keyboard.inch2pix(d[:2])
        kb_img = keyboard.image()
        # Draw scanpat
        for i in range(len(self.data)-1):
            pos1 = tuple(np.int0(self.data[i][:2]))
            pos2 = tuple(np.int0(self.data[i+1][:2]))
            cv2.line(kb_img, pos1, pos2, self.sac_color, 5)
        for d in self.data:
            cv2.circle(kb_img, tuple(np.int0(d[:2])), int(d[2]*self.max_fix_rad), self.fix_color, -1)
        # Resize image to show
        h, w = kb_img.shape[0:2]
        new_w = 1000
        kb_img = cv2.resize(kb_img, (new_w, new_w*h/w))
        cv2.imshow('Player', kb_img)
        while cv2.waitKey(0) != 27:
            pass
        cv2.destroyAllWindows()

if __name__=='__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generates ideal paths for given list of words.')
    parser.add_argument('folder', metavar='FOLDER',
                        help='trial folder containing data to be displayed')
    parser.add_argument('-r', '--redetect', action='store_true',
                        help='redetect keyboard corners')
    parser.add_argument('-u', '--unfiltered', action='store_true',
                        help="use unfiltered data (don't detect data)")
    args = parser.parse_args()

    ScanpathPlotter(args.folder, args.redetect, args.unfiltered).plot()
