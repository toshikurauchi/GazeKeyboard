# Word list from: http://svnweb.freebsd.org/base/head/share/dict/web2?view=co
# Word2 list from: http://www.manythings.org/vocabulary/lists/l/noll-about.php
# count_1w from: http://norvig.com/ngrams/
# Wikipedia word list from: http://www.monlp.com/2012/04/16/calculating-word-and-n-gram-statistics-from-a-wikipedia-corpora/
# google-10000-english list (we added 'minimization' and 'cognizant' to it) from: https://github.com/first20hours/google-10000-english

from dictionary import Dictionary
import os
import csv

def train(words_file, has_freq=False, limit=float("inf")):
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
    return dct

def add_freq(dct, freq_file):
    print 'Adding word frequencies'
    with open(freq_file, 'rb') as f:
        spamreader = csv.reader(f, delimiter='\t')
        for row in spamreader:
            word, freq = row
            if dct.contains(word):
                dct.add(word, int(freq))

def trained_dict():
    words_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'top100.csv')
    return train(words_file)

if __name__=='__main__':
    import sys

    words_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),'top100.csv')
    limit = float('inf')
    if len(sys.argv) > 1:
        words_file = sys.argv[1]
    if len(sys.argv) > 2:
        limit = int(sys.argv[2])
    has_freq = False
    if words_file in ['wikipedia_wordfreq.csv', 'count_1w.csv']:
        has_freq = True
    dct = train(words_file, has_freq, limit)
    print "Trained dictionary with %d words from %s"%(dct.root[dct._count],words_file)
