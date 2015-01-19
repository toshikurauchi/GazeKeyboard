# Word list from: http://svnweb.freebsd.org/base/head/share/dict/web2?view=co
# Word2 list from: http://www.manythings.org/vocabulary/lists/l/noll-about.php
# count_1w from: http://norvig.com/ngrams/
# Wikipedia word list from: http://www.monlp.com/2012/04/16/calculating-word-and-n-gram-statistics-from-a-wikipedia-corpora/

from dictionary import Dictionary
import pickle
import os
import csv

path = 'dict.pkl'
def train(words_file, has_freq, limit):
    dct = Dictionary()
    print 'Starting training'
    with open(words_file, 'rb') as f:
        count = 0
        if has_freq:
            spamreader = csv.reader(f, delimiter='\t')
            for row in spamreader:
                if count >= limit:
                    break
                word, freq = row
                dct.add(word, int(freq))
                count += 1
        else:
            for line in f:
                if count >= limit:
                    break
                dct.add(line.strip())
                count += 1
    print 'Word list trained'
    print 'Saving file...'
    with open(path, 'wb') as file:
        pickle.dump(dct, file, pickle.HIGHEST_PROTOCOL)
    print 'Dictionary saved to {f}'.format(f=path)
    return dct

def trained_dict():
    if not os.path.isfile(path):
        return train()
    with open(path, 'rb') as file:
        return pickle.load(file)

if __name__=='__main__':
    import sys

    words_file = 'words.txt'
    limit = float('inf')
    if len(sys.argv) > 1:
        words_file = sys.argv[1]
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
    has_freq = False
    if words_file in ['wikipedia_wordfreq.txt', 'count_1w.txt']:
        has_freq = True
    dct = train(words_file, has_freq, limit)
