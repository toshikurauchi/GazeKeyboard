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

    def extract(self):
        with open(self.keys_path, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            idx = 0
            for f in self.fixations:
                wk = self.keyboard.weighted_keys(f.pos)
                print 'Fixation ({t} s)'.format(t=f.duration) # I'm not 100% sure it is in seconds
                for k in wk:
                    print "Key: '{k}' weight: {w}".format(k=k.key, w=k.weight)
                    spamwriter.writerow([idx, k.key, k.weight, f.duration])
                idx += 1

if __name__=='__main__':
    import sys

    if len(sys.argv) < 2:
        print "USAGE: {p} TRIAL_FOLDER".format(p=sys.argv[0])
        sys.exit()

    folder = sys.argv[1]
    Extractor(folder).extract()
