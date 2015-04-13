import logging
from collections import namedtuple

Bucket = namedtuple('Bucket', ['pos', 'keys', 'layout', 'count'])
Bucket.__str__ = lambda self : 'Keys:%s, %d, (%.2f,%.2f)'%(self.keys, self.count, self.pos[0], self.pos[1])

def findCandidates(data, layout, smooth=False, dist_thresh=0.1, max_cands=5):
    if layout is None:
        logging.warn('Could not detect layout from filename')
    if data is None or len(data) == 0:
        logging.warn('Data not found')

    # Load candidates
    if 1: # Just in case it is too slow
        prev_cands = set()
        ref_cands = set()
        min_intersect = max_cands - 1
        cands = []
        count = 0
        for entry in data:
            # Take the max_cands keys that are closest to the current pointer position
            pos = entry.denorm_pos(layout.size)
            new_cands = sorted(layout.sorted_keys(pos)[0:max_cands])
            # Only consider keys within dist_thresh distance
            distSq = lambda p1, p2: (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
            new_cands = set([c.name for c in new_cands if distSq(c.pos, pos)/layout.size[0] < dist_thresh])
            # If intersection with the reference max_cands candidates in the current
            # group is greater or equal to min_intersect add to the current group,
            # otherwise start a new group
            if len(ref_cands.intersection(new_cands)) >= min_intersect:
                prev_cands = prev_cands.union(new_cands)
                count += 1
            else:
                if len(prev_cands) > 0:
                    cands.append(Bucket(pos,list(prev_cands),layout,count))
                prev_cands = new_cands
                ref_cands = new_cands
                min_intersect = max(len(prev_cands)-1,1)
                count = 1
        if len(prev_cands) > 0:
            cands.append(Bucket(pos,list(prev_cands),layout,count))
    else:
        cands = []
        for entry in data:
            pos = entry.denorm_pos(layout.size)
            keys = sorted(layout.sorted_keys(pos)[0:max_cands])
            cands.append(Bucket(pos, keys, layout, 1))
    return cands

if __name__=='__main__':
    import sys
    import os
    addpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../')
    sys.path.append(addpath)
    from KeyboardLayout import layoutFromFilename
    from DataFile import loadData

    if len(sys.argv) < 2:
        logging.error('USAGE: python %s FILENAME'%sys.argv[0])
        sys.exit()

    filename = sys.argv[1]
    data = loadData(filename)
    layout = layoutFromFilename(filename)

    cands = findCandidates(data, layout)
    for c in cands:
        print c
