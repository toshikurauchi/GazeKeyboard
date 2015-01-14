import numpy as np
from numpy.linalg import norm

class GazeData(object):
    def __init__(self, point, timestamp, confidence):
        self.point = point
        self.timestamp = timestamp
        self.confidence = confidence

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

def detect_fixations(gaze_list, fixation_thresh=20): # threshold in pixels
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
    return fixations