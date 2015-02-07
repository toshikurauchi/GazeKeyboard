from predict import load_char_sets
import os

hb = [
     ['a','b'],
     ['c','d'],
     ['e','f'],
     ['g','h'],
     ['i','j'],
     ['k','l'],
     ['m','n'],
     ['o','p'],
     ['q','r'],
     ['s','t'],
     ['u','v'],
     ['w','x'],
     ['y','z'],
     ]

correct = ['computer', 'minimization', 'successfully', 'cognizant']

vid = '../../videos'
sbjs = [os.path.join(vid,s) for s in os.listdir(vid)]
sbjs = [s for s in sbjs if os.path.isdir(s)]
for sbj in sbjs:
    trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
    trials = [t for t in trials if os.path.isdir(t)]
    for trial in trials:
        print 'Test for {f}'.format(f=trial)
        buckets = load_char_sets(os.path.join(trial,'keys.csv'))
        chars = set([k for c in buckets for k in c.keys()])
        for word in correct:
            count = 0
            for char in word:
                if char not in chars:
                    count += 1
            print word, count

        hash = [False for i in range(len(hb))]
        for i in range(len(hb)):
            h = hb[i]
            for c in h:
                if c in chars:
                    hash[i] = True
                    break
        print sum(hash)/13.
        print
