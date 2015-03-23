import numpy as np
from numpy.linalg import norm
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from levenshtein import levenshtein_iter, find_used, fill_gaps
from keyboard_layout import PrintedKeyboardLayout
keyboard = PrintedKeyboardLayout()

class Trie(object):
    ''' Based on http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python '''
    def __init__(self, words=[]):
        self._count = '_count_'
        self._end = '_end_'
        self.max_length = 0
        self.flags = [self._count, self._end]
        self.root = {self._count:0}
        for word in words:
            self.add(word)

    def add(self, word, count=1):
        word = word.lower().strip()
        length = len(word)
        if length > self.max_length:
            self.max_length = length
        cur_dict = self.root
        cur_dict[self._count] += count
        for letter in word:
            cur_dict = cur_dict.setdefault(letter, {self._count:0})
            cur_dict[self._count] += count
        cur_dict = cur_dict.setdefault(self._end, {self._count:0})
        cur_dict[self._count] += count

    def contains(self, word):
        cur_dict = self.root
        for letter in word:
            if letter in cur_dict:
                cur_dict = cur_dict[letter]
            else:
                return False
        else:
            if self._end in cur_dict:
                return True
            else:
                return False

class Dictionary(Trie):
    def __init__(self, words=[]):
        super(Dictionary, self).__init__(words)
        self._ldist = '__ldist__'
        self._eidx = '__eidx__'
        self.flags.extend([self._ldist, self._eidx])
        self.enter_idx = [None for i in range(self.max_length)]
        self._reset(self.root)

    def _reset(self, cur_dict, depth=0):
        cur_dict[self._ldist] = depth
        cur_dict[self._eidx] = []
        for key in cur_dict.keys():
            if key not in self.flags:
                self._reset(cur_dict[key], depth+1)

    def find_candidates(self, char_sets, reset=False):
        if reset:
            self.enter_idx = [None for i in range(self.max_length)]
            self._reset(self.root)
        return self._find_candidates_rec(0, self.root, '', '', char_sets)

    def _find_candidates_rec(self, depth, cur_dict, word, char, char_sets, a00_dist=0, a01_dist=0):
        cand = set()
        a10_dist = cur_dict[self._ldist]
        if depth > 0:
            cur_dict[self._ldist], me = levenshtein_iter(char, char_sets[-1], a00_dist, a01_dist, a10_dist)
            if me:
                cur_dict[self._eidx].append((len(char_sets)-1, cur_dict[self._ldist]))
            self.enter_idx[depth-1] = cur_dict[self._eidx]
        word += char
        if cur_dict[self._ldist] > 2:
            return cand
        if self._end in cur_dict.keys(): # Is a word
            #if word not in ['the','and','of','to','a','as','in','on','for','is','that','i','by','with','you','it','not','or','be','are','this','from','at','your','new','more','an','was','we','will','home']: # TODO REMOVE THIS CONDITION!
            used = find_used(self.enter_idx, depth, cur_dict[self._ldist])
            filled = fill_gaps(word, used, char_sets, keyboard.key_center)
            cand.add(WordCandidate(word, cur_dict[self._end][self._count], cur_dict[self._ldist], char_sets, used, filled))
        for key in cur_dict.keys():
            if key not in self.flags:
                cand.update(self._find_candidates_rec(depth+1, cur_dict[key], word, key, char_sets, a10_dist, cur_dict[self._ldist]))
        return cand

def path_weight(word, buckets, indices):
    if not word or not buckets or not indices:
        return 0
    prev_key_pos = np.array(buckets[0]['_p'])
    prev_pos = prev_key_pos
    distances = []
    weights = []
    cur_bucket = 0
    total_dist = 0
    for idx in indices:
        stop_bucket = idx[1]
        dist = 0
        while cur_bucket <= stop_bucket:
            cur_pos = np.array(buckets[cur_bucket]['_p'])
            dist += norm(cur_pos-prev_pos)
            prev_pos = cur_pos
            cur_bucket += 1
        cur_bucket = stop_bucket
        key_pos = np.array(keyboard.key_center(word[idx[0]]))
        key_dist = norm(cur_pos-prev_key_pos)
        distances.append((key_dist, dist))
        if key_dist and len(distances) > 1: # Isn't the first
            weights.append(dist)
        prev_key_pos = cur_pos
        prev_pos = prev_key_pos
    # Account for the rest of the buckets
    dist = 0
    while cur_bucket < len(buckets):
        cur_pos = np.array(buckets[cur_bucket]['_p'])
        dist += norm(cur_pos-prev_pos)
        prev_pos = cur_pos
        cur_bucket += 1
    key_dist = norm(cur_pos-prev_key_pos)
    total_dist += dist
    distances.append((key_dist, dist))

    used_ratio = 0
    path_w = 0
    if total_dist:
        used_ratio = (total_dist-(distances[0][1]+distances[-1][1]))/total_dist
    distances = [0 if d[1] == 0 else min(d[0]/d[1], d[1]/d[0]) for d in distances[1:-1] if d[0] != 0]
    if distances:
        path_w = np.average(distances, weights=weights)
    return path_w, used_ratio, distances

class WordCandidate(object):
    def __init__(self, word, freq, ldist, char_sets, used, filled):
        self.word = word
        self.freq = freq
        self.size_w = (len(word)-ldist)/float(len(char_sets))
        self.weighted_time = sum([char_sets[u[1]][word[u[0]]]*char_sets[u[1]]['_t'] for u in used])
        self.path_w, self.used_path_w, self.distances = path_weight(word, char_sets, filled)

    def __eq__(self, other):
        return self.word.__eq__(other.word)

    def __hash__(self, *args, **kwargs):
        return self.word.__hash__(*args, **kwargs)

