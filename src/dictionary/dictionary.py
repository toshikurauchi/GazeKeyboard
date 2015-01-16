import numpy as np

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

def fit_keys(keys, char_sets):
    i = 0
    weights = []
    for k in keys:
        while i < len(char_sets) and k not in char_sets[i].keys():
            i += 1
        if i < len(char_sets):
            w = char_sets[i][k]
            weights.append(w)
            char_sets[i] = {k:w} # Only the chosen character can be repeated
    return char_sets[i:], weights

class Dictionary(Trie):
    def __init__(self, words=[]):
        super(Dictionary, self).__init__(words)

    def find_candidates(self, char_sets):
        return self._find_candidates_rec(self.root, '', '', char_sets, [])

    def _find_candidates_rec(self, cur_dict, prefix, checked_prefix, char_sets, weights):
        cand = set()
        if len(char_sets) == 0:
            return cand
        if self._end in cur_dict.keys():
            char_sets, new_weights = fit_keys(prefix[len(checked_prefix):], char_sets)
            weights = weights + new_weights
            if len(char_sets) == 0:
                return cand
            cand.add(WordCandidate(prefix, cur_dict[self._end][self._count], np.mean(weights)))
            checked_prefix = prefix
        for key in cur_dict.keys():
            if key not in self.flags:
                cand.update(self._find_candidates_rec(cur_dict[key], prefix+key, checked_prefix, char_sets, weights))
        return cand

class WordCandidate(object):
    def __init__(self, word, freq, dist):
        self.word = word
        self.freq = freq
        self.dist = dist

    def __eq__(self, other):
        return self.word.__eq__(other.word)

    def __hash__(self, *args, **kwargs):
        return self.word.__hash__(*args, **kwargs)

