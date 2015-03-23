import csv
import os
import sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from train_dictionary import trained_dict
from util import load_char_sets

LANGUAGE_WEIGHT = 0.1
LENGTH_WEIGHT   = 0.4
TIME_WEIGHT     = 0.1
PATH_WEIGHT     = 0.4

def add_prob(cand, max_freq, fix_count):
    cand.freq_w = cand.freq/float(max_freq)
    cand.p = LANGUAGE_WEIGHT * cand.freq_w \
           + LENGTH_WEIGHT * cand.size_w \
           + TIME_WEIGHT * cand.weighted_time \
           + PATH_WEIGHT * cand.path_w
    return cand

def print_cand(c):
    args = {'w':c.word, 'f':c.freq_w, 't':c.weighted_time,
            's':c.size_w, 'p':c.path_w, 'u': c.used_path_w, 'P':c.p, 'd':c.distances}
    print '{w:<13}: freq={f:.2f}, time={t:.2f}, size={s:.2f}, path={p:.2f}, u_path={u:.2f}, P={P:.2f}, {d}'.format(**args)

def predict(dct, trial):
    keys_path = os.path.join(trial, 'keys.csv')
    char_sets = load_char_sets(keys_path)
    fix_count = len(char_sets)
    is_first = True
    cands = set()
    for i in range(len(char_sets)):
        cands = dct.find_candidates(char_sets[:i+1], is_first)
        is_first = False
    if len(cands) > 0:
        max_freq = max([c.freq for c in cands])
        cands = map(lambda c: add_prob(c, max_freq, fix_count), cands)
        cands = sorted(cands, key=lambda c: c.p, reverse=True)
        for cand in cands[:10]:
            print_cand(cand)
    return cands

if __name__=='__main__':
    import sys

    dct = trained_dict()
    print 'Dictionary initialized'

    if len(sys.argv) > 1:
        trial = sys.argv[1]
        predict(dct, trial)
    else:
        vid = '../../videos'
        sbjs = [os.path.join(vid,s) for s in os.listdir(vid)]
        sbjs = [s for s in sbjs if os.path.isdir(s)]
        words = ['from', 'snowboard', 'toolkit', 'violin', 'arcade', 'let']
        for sbj in sbjs:
            trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
            trials = [t for t in trials if os.path.isdir(t)]
            for trial in trials:
                cur_word = None
                for word in words:
                    if word in trial:
                        cur_word = word
                        break
                if cur_word is None:
                    continue
                print 'Predictions for {f}'.format(f=trial)
                cands = predict(dct, trial)
                found = [c for c in cands if word in c.word]
                print 'Similar candidates:' if len(found)>0 else 'No candidates found :('
                for f in found:
                    print_cand(f)
                print

