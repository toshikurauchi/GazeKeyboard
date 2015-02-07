import numpy as np
from numpy.linalg import norm

class GazeData(object):
    def __init__(self, point, timestamp, confidence):
        self.point = point
        self.timestamp = timestamp
        self.confidence = confidence

    @classmethod
    def from_values(cls, values):
        return cls(values[0], values[1], values[2])

    def values(self):
        return [self.point, self.timestamp, self.confidence]

class Fixation(object):
    def __init__(self, pos=None, t0=None, duration=0):
        self.pos = pos
        self.t0 = t0
        self.duration = duration
        self.data = []

    @classmethod
    def from_values(cls, values):
        pos = np.array(values[0:2]).ravel()
        return cls(pos, values[2], values[3])

    def add_data(self, gaze_data):
        self.data.append(gaze_data)

        # Update times
        tstamp = gaze_data.timestamp
        if self.t0 is None:
            self.t0 = tstamp
        self.duration = tstamp - self.t0

        # Update position
        self.pos = np.mean([d.point for d in self.data], 0)

    def values(self):
        return [self.pos[0], self.pos[1], self.t0, self.duration]

def detect_fixations(gaze_list, fixation_thresh=2): # threshold in inches
    fixations = []
    cur_fix   = None
    for i in range(len(gaze_list)-1):
        g1,g2 = gaze_list[i],gaze_list[i+1]
        dist = norm(g2.point-g1.point)
        if dist < fixation_thresh:
            if cur_fix is None:
                cur_fix = Fixation()
            cur_fix.add_data(g1)
        elif cur_fix is not None:
            fixations.append(cur_fix)
            cur_fix = None
    if cur_fix is not None:
        fixations.append(cur_fix)
    return fixations

if __name__=='__main__':
    import argparse
    from util import list_trial_folders
    import os

    parser = argparse.ArgumentParser(description='Generates ideal paths for given list of words.')
    parser.add_argument('folders', metavar='FOLDER', nargs='*',
                        help='trial folder(s) containing data to be processed')
    args = parser.parse_args()

    folders = args.folders
    if not folders:
        folders = list_trial_folders('../videos')
    for f in folders:
        data_path = os.path.join(f, 'keyboard_gaze.npy')
        fix_path = os.path.join(f, 'keyboard_fixations.npy')
        if not os.path.isfile(data_path):
            continue
        print 'Processing {f}...'.format(f=data_path)
        data = np.load(data_path)
        gaze = [GazeData.from_values(d) for d in data]
        fixations = detect_fixations(gaze)
        np.save(fix_path, [f.values() for f in fixations])
