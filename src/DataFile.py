import csv
import abc
import logging
import re

class Data(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, tstamp):
        self._tstamp = tstamp

    @property
    def tstamp(self):
        return self._tstamp

    @abc.abstractmethod
    def pos(self):
        return

    def denorm_pos(self, size):
        x, y = self.pos()
        w, h = size
        return (x*w, y*h)

class GazeData(Data):
    def __init__(self, tstamp, raw, smooth, is_fix):
        super(GazeData, self).__init__(tstamp)
        self._raw = raw
        self._smooth = smooth
        self._is_fix = is_fix

    def __str__(self):
        return 'Gaze: %d, %s, %s, %s'%(self._tstamp, self._raw,
                                       self._smooth, self._is_fix)

    def pos(self, smooth=False):
        if smooth: return self._smooth
        return self._raw

    @property
    def is_fix(self):
        return self._is_fix

class MouseData(Data):
    def __init__(self, tstamp, pos):
        self._tstamp = tstamp
        self._pos = pos

    def __str__(self):
        return 'Mouse: %d, %s'%(self._tstamp, self._pos)

    def pos(self, smooth=False):
        return self._pos

def loadData(filename):
    is_gaze = re.search('[\\\/]gaze[\\\/]', filename) is not None
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # Skip header
        for line in reader:
            # Check line size
            format_size = 6 if is_gaze else 3
            if len(line) != format_size:
                logging.warn('Invalid format for line %s'%line)
                continue
            entry = [int(line[0]), (float(line[1]), float(line[2]))]
            if is_gaze:
                entry.append((float(line[3]), float(line[4])))
                entry.append(int(line[5]) == 1)
                data.append(GazeData(*entry))
            else:
                data.append(MouseData(*entry))
    return data

if __name__=='__main__':
    import sys

    if len(sys.argv) < 2:
        logging.error('USAGE: python %s FILENAME'%sys.argv[0])
        sys.exit()

    loadData(sys.argv[1])