import csv
import logging
from collections import namedtuple
import os

_layouts = None

Key = namedtuple('Key', ['name', 'pos'])

class KeyboardLayout(object):
    def __init__(self, name):
        self.name = name
        self._keys = {}
        self.size = None

    def __str__(self):
        return '%s: %d keys'%(self.name,len(self._keys))

    def key_pos(self, key):
        if key in self._keys: return self._keys[key].pos
        return None

    def add_key(self, key):
        if key.name in self._keys:
            logging.warning('Key %s already added!'%key.name)
        self._keys[key.name] = key

    def sorted_keys(self, ref_point):
        dist = lambda k: (k.pos[0]-ref_point[0])**2 + (k.pos[1]-ref_point[1])**2
        keys = sorted(self._keys.values(), key=dist)
        return [k for k in keys]

def layouts():
    '''Load layouts with key coordinates'''
    global _layouts
    if _layouts is not None:
        return _layouts

    coordinates_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                    '../layout/Coordinates.csv')
    _layouts = [KeyboardLayout('DoubleRing'),
                KeyboardLayout('SingleRing'),
                KeyboardLayout('Phone'),
                KeyboardLayout('QWERTY')]

    with open(coordinates_file) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        size = next(reader)
        for layout in _layouts:
            layout.size = (float(size[0]), float(size[1]))
        for line in reader:
            char = line[0]
            points = [(float(line[2*i+1]), float(line[2*i+2])) for i in range(len(_layouts))]
            for i in range(len(points)):
                k = Key(char.lower(), points[i])
                _layouts[i].add_key(k)

    # Transform list in dict
    _layouts = {l.name: l for l in _layouts}
    return _layouts

def layoutFromFilename(filename):
    ls = layouts()
    for l in ls:
        if l in filename:
            return ls[l]
    return None

if __name__=='__main__':
    ls = layouts()
    for l in ls:
        print ls[l]

    f = 'test/data/SingleRing/problem1.csv'
    print 'Layout from filename', f, layoutFromFilename(f)
    f = 'test/data/NO_LAYOUT/problem1.csv'
    print 'Layout from filename', f, layoutFromFilename(f)
