import csv
import os

from train_dictionary import trained_dict

def load_char_sets(keys_path):
    with open(keys_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cur_id = -1
        char_sets = []
        for row in spamreader:
            new_id, char = int(row[0]), row[1]
            if new_id == cur_id:
                cur_char_set.append(char)
            else:
                cur_id = new_id
                cur_char_set = [char]
                char_sets.append(cur_char_set)
    return char_sets

def predict(dct, trial):
    keys_path = os.path.join(trial, 'keys.csv')
    char_sets = load_char_sets(keys_path)
    cands = dct.find_candidates(char_sets)
    cands = sorted(cands, key=lambda c: len(c.word), reverse=True)
    cands = sorted(cands[:10], key=lambda c: c.freq, reverse=True)
    for cand in cands:
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
        for sbj in sbjs:
            trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
            trials = [t for t in trials if os.path.isdir(t)]
            for trial in trials:
                print 'Predictions for {f}'.format(f=trial)
                predict(dct, trial)
                print

