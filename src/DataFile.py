import csv
import logging
import re

class Data(object):
    def __init__(self, tstamp, pos):
        self._tstamp = tstamp
        self._pos = pos

    @property
    def tstamp(self):
        return self._tstamp

    def pos(self):
        return self._pos
    
    def __str__(self):
        return 'Data: %d, %s'%(self._tstamp, self._pos)

    def denorm_pos(self, size):
        x, y = self.pos()
        w, h = size
        return (x*w, y*h)
        
    def norm_pos_keep_ratio(self, size):
        x, y = self.pos()
        w, h = size
        return (x, y*h/w)

def loadData(filename):
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader) # Skip header
        for line in reader:
            # Check line size
            format_size = 3
            if len(line) != format_size:
                logging.warn('%s:Invalid format for line %s'%(filename, line))
                continue
            entry = [float(line[0]), (float(line[1]), float(line[2]))]
            data.append(Data(*entry))
    return data

if __name__=='__main__':
    import sys

    if len(sys.argv) < 2:
        logging.error('USAGE: python %s FILENAME'%sys.argv[0])
        sys.exit()

    loadData(sys.argv[1])