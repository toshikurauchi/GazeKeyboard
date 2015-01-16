# Word list from: http://svnweb.freebsd.org/base/head/share/dict/web2?view=co
# Wikipedia word list from: http://www.monlp.com/2012/04/16/calculating-word-and-n-gram-statistics-from-a-wikipedia-corpora/

from dictionary import Dictionary
import pickle
import os
import csv

path = 'dict.pkl'
def train():
    dct = Dictionary()
    print 'Starting training'
    with open('words.txt', 'rb') as f:
        for line in f:
            dct.add(line.strip())
    print 'Word list trained'
    with open('wikipedia_wordfreq.txt') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='\t')
        for row in spamreader:
            word, freq = row
            if dct.contains(word):
                dct.add(word, int(freq))
    print 'Wikipedia words trained'
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
    dct = train()
    for cand in dct.find_candidates([['a'],['a'],['c'],['r','n'],['o','i'],['n']]):
        print cand.word, cand.freq
