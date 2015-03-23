import os
import numpy as np
import csv

from util import load_or_detect_fixations
from keyboard import PrintedKeyboard

class Extractor(object):
    def __init__(self, folder):
        self.keys_path = os.path.join(folder, 'keys.csv')
        self.fixations = load_or_detect_fixations(folder)
        self.keyboard = PrintedKeyboard()

    def extract(self, verbose=True):
        with open(self.keys_path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            idx = 0
            for f in self.fixations:
                wk = self.keyboard.weighted_keys(f.pos)
                if verbose:
                    print 'Fixation ({t} s)'.format(t=f.duration) # I'm not 100% sure it is in seconds
                for k in wk:
                    if verbose:
                        print "Key: '{k}' weight: {w}".format(k=k.key, w=k.weight)
                    spamwriter.writerow([idx, k.key, k.weight, f.duration, f.pos[0], f.pos[1]])
                idx += 1

if __name__=='__main__':
    import sys

    if len(sys.argv) > 1:
        folder = sys.argv[1]
        Extractor(folder).extract()
    else:
        vid = '../videos'
        sbjs = [os.path.join(vid,s) for s in os.listdir(vid)]
        sbjs = [s for s in sbjs if os.path.isdir(s)]
        for sbj in sbjs:
            trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
            trials = [t for t in trials if os.path.isdir(t)]
            for trial in trials:
                print 'Extracting key candidates for {f}'.format(f=trial)
                Extractor(trial).extract(verbose=False)
