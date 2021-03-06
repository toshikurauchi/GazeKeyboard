import numpy as np
from numpy.linalg import norm
from levenshtein import levenshtein_iter

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
        self.flags.extend([self._ldist])
        self._reset(self.root)

    def _reset(self, cur_dict, depth=0):
        cur_dict[self._ldist] = 0 if depth == 0 else float('inf')
        for key in cur_dict.keys():
            if key not in self.flags:
                self._reset(cur_dict[key], depth+1)

    def find_candidates(self, buckets, reset=False):
        if reset:
            self._reset(self.root)
        return self._find_candidates_rec(0, self.root, '', '', buckets)

    def _find_candidates_rec(self, depth, cur_dict, word, char, buckets, a00_dist=0, a01_dist=0):
        cand = set()
        a10_dist = cur_dict[self._ldist]
        if depth > 0:
            cur_dict[self._ldist] = levenshtein_iter(char, buckets[-1], a00_dist, a01_dist, a10_dist)
        word += char
        #if cur_dict[self._ldist] > 2:
        #    return cand
        if self._end in cur_dict.keys(): # Is a word
            cand.add(WordCandidate(word, cur_dict[self._end][self._count], cur_dict[self._ldist], buckets))
        for key in cur_dict.keys():
            if key not in self.flags:
                cand.update(self._find_candidates_rec(depth+1, cur_dict[key], word, key, buckets, a10_dist, cur_dict[self._ldist]))
        return cand

class WordCandidate(object):
    def __init__(self, word, freq, ldist, buckets):
        self.word = word
        self.freq = freq
        self.ldist = ldist
        self.size_w = (len(word)-ldist)/float(len(buckets))

    def __eq__(self, other):
        return self.word.__eq__(other.word)

    def __hash__(self, *args, **kwargs):
        return self.word.__hash__(*args, **kwargs)

    def __str__(self, *args, **kwargs):
        return self.word
