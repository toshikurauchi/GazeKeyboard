import numpy as np

from levenshtein import levenshtein

class Trie(object):
    ''' Based on http://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python '''
    def __init__(self, words=[]):
        self._count = '_count_'
        self._end = '_end_'
        self.flags = [self._count, self._end]
        self.root = {self._count:0}
        for word in words:
            self.add(word)

    def add(self, word, count=1):
        word = word.lower().strip()
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

def remove_duplications(word):
    if len(word) == 0:
        return word
    new_w = word[0]
    for i in range(len(word)-1):
        if word[i] != word[i+1]:
            new_w += word[i+1]
    return new_w

class Dictionary(Trie):
    def __init__(self, words=[]):
        super(Dictionary, self).__init__(words)

    def find_candidates(self, char_sets):
        return self._find_candidates_rec(self.root, '', '', char_sets, 0)

    def _find_candidates_rec(self, cur_dict, checked_prefix, prefix, char_sets, cur_dist):
        cand = set()
        if self._end in cur_dict.keys():
            dist, _, idx = levenshtein(remove_duplications(prefix), char_sets)
            cur_dist += dist
            word = checked_prefix+prefix
            if dist < 4:
                checked_prefix = word
                prefix = ''
                cand.add(WordCandidate(checked_prefix, cur_dict[self._end][self._count]))
                if len(idx) == 0:
                    return cand
                char_sets = char_sets[idx[-1]:]
            else:
                return cand
        for key in cur_dict.keys():
            if key not in self.flags:
                cand.update(self._find_candidates_rec(cur_dict[key], checked_prefix, prefix+key, char_sets, cur_dist))
        return cand

class WordCandidate(object):
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def __eq__(self, other):
        return self.word.__eq__(other.word)

    def __hash__(self, *args, **kwargs):
        return self.word.__hash__(*args, **kwargs)

