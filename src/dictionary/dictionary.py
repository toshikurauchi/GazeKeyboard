import numpy as np

from levenshtein import levenshtein

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

    def find_candidates(self, char_sets):
        self.v = [[0]*(len(char_sets)+1) for i in range(self.max_length + 1)]
        self.cur_dur = sum([c[c.keys()[0]]['t'] for c in char_sets])
        return self._find_candidates_rec(0, self.root, '', '', char_sets)

    def _find_candidates_rec(self, depth, cur_dict, checked_prefix, prefix, char_sets, last_dist=0, used_word=''):
        cand = set()
        dist, last_dist = levenshtein(prefix, char_sets, last_dist, self.v[depth], self.v[depth+1])
        checked_prefix += prefix
        prefix = ''
        if dist > 2:
            return cand
        if self._end in cur_dict.keys(): # Is a word
            cand.add(WordCandidate(checked_prefix, cur_dict[self._end][self._count], (len(checked_prefix)-dist)/float(len(char_sets))))
        for key in cur_dict.keys():
            if key not in self.flags:
                cand.update(self._find_candidates_rec(depth+1, cur_dict[key], checked_prefix, prefix+key, char_sets, last_dist, used_word))
        return cand

class WordCandidate(object):
    def __init__(self, word, freq, size_w):
        self.word = word
        self.freq = freq
        self.size_w = size_w

    def __eq__(self, other):
        return self.word.__eq__(other.word)

    def __hash__(self, *args, **kwargs):
        return self.word.__hash__(*args, **kwargs)

