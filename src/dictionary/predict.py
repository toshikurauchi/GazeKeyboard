import csv
import os

from train_dictionary import trained_dict

LENGTH_WEIGHT   = 0.2
LANGUAGE_WEIGHT = 0.5
TIME_WEIGHT     = 0.3

def load_char_sets(keys_path):
    with open(keys_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cur_id = -1
        char_sets = []
        for row in spamreader:
            new_id, char, weight, time = int(row[0]), row[1], float(row[2]), float(row[3])
            if new_id == cur_id:
                cur_char_set[char] = {'w':weight,'t':time}
            else:
                cur_id = new_id
                cur_char_set = {char:{'w':weight,'t':time}}
                char_sets.append(cur_char_set)
    return char_sets

def add_prob(cand, max_freq, fix_count):
    cand.p = LANGUAGE_WEIGHT * cand.freq/float(max_freq) \
           + LENGTH_WEIGHT * cand.size_w \
           + TIME_WEIGHT * cand.weighted_time
    return cand

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
            print cand.word, cand.freq/float(max_freq), cand.size_w, cand.p
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
                found = [c for c in cands if c.word in word or word in c.word]
                print 'Similar candidates:' if len(found)>0 else 'No candidates found :('
                for f in found:
                    print f.word, f.freq, f.size_w, f.p
                print

