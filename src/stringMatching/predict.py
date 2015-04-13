import csv
import os
import math
import sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from train_dictionary import trained_dict

LANGUAGE_WEIGHT = 0.1
LENGTH_WEIGHT   = 0.4
TIME_WEIGHT     = 0.1
PATH_WEIGHT     = 0.4

def print_cand(c):
    args = {'w':c.word, 'dist':c.ldist}
    print '{w:<13}: Dist={dist:.2f}'.format(**args)

def predict(dct, buckets):
    is_first = True
    cands = set()
    for i in range(len(buckets)):
        cands = dct.find_candidates(buckets[:i+1], is_first)
        is_first = False
    if len(cands) > 0:
        max_len = float(max([len(c.word) for c in cands]))
        cands = [c for c in cands if c.ldist < 0.2]
        compute_weight = lambda c: len(c.word)/max_len * math.exp(-10*c.ldist)
        cands.sort(key=compute_weight, reverse=True)
    return cands

if __name__=='__main__':
    import sys
    import os
    import re
    from CandidateKey import findCandidates
    from KeyboardLayout import layoutFromFilename
    from DataFile import loadData

    dct = trained_dict()
    print 'Dictionary initialized'

    N_TOP = 10
    if len(sys.argv) > 1:
        trial = sys.argv[1]
        data = loadData(trial)
        layout = layoutFromFilename(trial)
        buckets = findCandidates(data, layout)
        cands = predict(dct, buckets)
        for c in cands[:N_TOP]:
            print_cand(c)
    else:
        rec = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../../data/recordings/')
        sbjs = [os.path.join(rec,s) for s in os.listdir(rec)]
        sbjs = [s for s in sbjs if os.path.isdir(s)]
        modes = [os.path.join(sbj,m) for sbj in sbjs for m in os.listdir(sbj)]
        modes = [m for m in modes if os.path.isdir(m)]
        layouts = [os.path.join(m, l) for m in modes for l in os.listdir(m)]
        layouts = [l for l in layouts if os.path.isdir(l)]
        def extract_word(filename):
            match = re.search('(.*)[0-9]+.csv', os.path.split(filename)[1])
            if match: return match.group(1)
            return None
        words = [os.path.join(l, w) for l in layouts for w in os.listdir(l)]
        words = [(extract_word(w), w) for w in words]
        words = [w for w in words if w[0] is not None]
        for w in words:
            cur_word = w[0]
            match = re.search('data\/recordings\/(.*)', w[1])
            if match is None: continue
            print 'Predictions for {f}'.format(f=match.group(1))
            data = loadData(w[1])
            layout = layoutFromFilename(w[1])
            buckets = findCandidates(data, layout)
            predict(dct, buckets)
            cands = predict(dct, buckets)
            for c in cands[:N_TOP]:
                print_cand(c)

