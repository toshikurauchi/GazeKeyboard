import csv
import os

from train_dictionary import trained_dict

DISTANCE_WEIGHT = 0.2
LENGTH_WEIGHT = 0.5
LANGUAGE_WEIGHT = 0.3

def load_char_sets(keys_path):
    with open(keys_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cur_id = -1
        char_sets = []
        for row in spamreader:
            new_id, char, weight = int(row[0]), row[1], float(row[2])
            if new_id == cur_id:
                cur_char_set[char] = weight
            else:
                cur_id = new_id
                cur_char_set = {char:weight}
                char_sets.append(cur_char_set)
    return char_sets

def prob(cand, total_freq, fix_count):
    return LANGUAGE_WEIGHT * cand.freq/float(total_freq)

def predict(dct, trial):
    keys_path = os.path.join(trial, 'keys.csv')
    char_sets = load_char_sets(keys_path)
    fix_count = len(char_sets)
    cands = dct.find_candidates(char_sets)
    total_freq = sum([c.freq for c in cands])
    cands = sorted(cands, key=lambda c: prob(c, total_freq, fix_count), reverse=True)
    for cand in cands[:10]:
        print cand.word, cand.freq
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
        correct = ['computer', 'minimization', 'successfully', 'cognizant']
        for sbj in sbjs:
            trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
            trials = [t for t in trials if os.path.isdir(t)]
            for trial in trials:
                print 'Predictions for {f}'.format(f=trial)
                cands = predict(dct, trial)
                found = len([c for c in cands if c.word in correct]) > 0
                print 'Found!' if found else 'Not found :('
                print

