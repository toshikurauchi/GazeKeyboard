import csv
import os

from util import load_or_detect_fixations

if __name__ =='__main__':
    vid = '../videos'
    sbjs = [os.path.join(vid,s) for s in os.listdir(vid)]
    sbjs = [s for s in sbjs if os.path.isdir(s)]
    for sbj in sbjs:
        trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
        trials = [t for t in trials if os.path.isdir(t)]
        for trial in trials:
            with open(os.path.join(trial, 'fixations.csv'), 'wb') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter=',')
                fixations = load_or_detect_fixations(trial)
                for fixation in fixations:
                    spamwriter.writerow([fixation.t0, fixation.pos[0], fixation.pos[1]])