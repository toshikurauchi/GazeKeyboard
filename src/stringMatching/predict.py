import csv
import os
import math
import sys,inspect
from _collections import defaultdict
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from train_dictionary import trained_dict

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
    import logging

    from CandidateKey import findCandidates
    from KeyboardLayout import layoutFromFilename
    from DataFile import loadData

    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def extract_word(filename):
        match = re.search('(.*)([0-9]+).csv', os.path.split(filename)[1])
        if match: return match.group(1), match.group(2)
        return None, None

    def format_cand(c):
        args = {'w':c.word, 'dist':c.ldist}
        return '{w:<13}: Dist={dist:.2f}'.format(**args)

    def candidate_pos(word, cands):
        idx = len(cands)
        for i in range(len(cands)):
            if cands[i].word == word:
                idx = i
                break
        if idx < len(cands): logger.info('Found at position %d'%idx)
        else: logger.info('Not found :(')
        for c in cands[:idx+1]:
            logger.info(format_cand(c))
        return idx

    dct = trained_dict()
    logger.info('Dictionary initialized')

    if len(sys.argv) > 1:
        trial = sys.argv[1]
        data = loadData(trial)
        layout_name = layoutFromFilename(trial)
        buckets = findCandidates(data, layout_name)
        if buckets is None: sys.exit(0)
        cands = predict(dct, buckets)
        candidate_pos(extract_word(trial)[0], cands)
    else:
        results = {}
        rec = os.path.join(os.path.dirname(os.path.realpath(__file__)),'../../data/recordings/')
        sbjs = [s for s in os.listdir(rec) if os.path.isdir(os.path.join(rec, s)) and s != 'old']
        for sbj in sbjs:
            results[sbj] = {}
            sbj_folder = os.path.join(rec, sbj)
            modes = [m for m in os.listdir(sbj_folder) if os.path.isdir(os.path.join(sbj_folder, m))]
            for mode in modes:
                results[sbj][mode] = {}
                mode_folder = os.path.join(sbj_folder, mode)
                layouts = [l for l in os.listdir(mode_folder) if os.path.isdir(os.path.join(mode_folder, l))]
                for layout_name in layouts:
                    results[sbj][mode][layout_name] = {}
                    layout_folder = os.path.join(mode_folder, layout_name)
                    word_files = [w for w in os.listdir(layout_folder) if w.endswith('.csv')]
                    for word_file in word_files:
                        word, trial = extract_word(word_file)
                        word_file = os.path.join(layout_folder, word_file)
                        if word is None: continue
                        data = loadData(word_file)
                        layout = layoutFromFilename(word_file)
                        buckets = findCandidates(data, layout)
                        if buckets is None: continue
                        predict(dct, buckets)
                        cands = predict(dct, buckets)
                        if word not in results[sbj][mode][layout_name]:
                            results[sbj][mode][layout_name][word] = {}
                        print 'here'
                        logger.info('Predictions for %s, %s, %s, %s'%(sbj, mode, layout_name, word))
                        idx = candidate_pos(word, cands)
                        results[sbj][mode][layout_name][word][trial] = {'idx': idx, 'found': idx < len(cands)}
        with open('predictions.csv', 'wb') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['sbj', 'mode', 'layout', 'word', 'trial', 'found_idx', 'found'])
            for sbj in results:
                for mode in results[sbj]:
                    for layout in results[sbj][mode]:
                        for word in results[sbj][mode][layout]:
                            for trial in results[sbj][mode][layout][word]:
                                result = results[sbj][mode][layout][word][trial]
                                idx = result['idx']
                                found = result['found']
                                writer.writerow([sbj, mode, layout, word, trial, idx, found])
