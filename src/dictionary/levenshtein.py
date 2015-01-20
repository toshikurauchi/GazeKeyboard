# Source: http://en.wikipedia.org/wiki/Levenshtein_distance

def levenshtein(word, fixations):
    # degenerate cases
    if len(word) == 0: return 0
    if len(fixations) == 0: return len(word)

    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty word
    # the distance is always zero as the deletion of a fixation has cost 0
    # (IMPORTANT: this is different from the lenveshtein distance!)
    v0 = [0]*(len(fixations)+1)
    v1 = [0]*(len(fixations)+1)
    last_dist = 0
    used_word = ''

    for i in range(len(word)):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        #   edit distance is delete (i+1) chars in word to match empty fixation list
        #   cost of deleting char in word is 1
        v1[0] = v0[0] + 1

        # use formula to fill in the rest of the row
        for j in range(len(fixations)):
            cost = 0 if word[i] in fixations[j] else 1
            # IMPORTANT: the following line is different from the levenshtein
            # distance. We don't penalize deletions from fixations list.
            v1[j + 1] = min([v1[j], v0[j + 1] + 1, v0[j] + cost])

        if last_dist == v1[-1]:
            used_word += word[i]
        last_dist = v1[-1]

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(len(fixations) + 1):
            v0[j] = v1[j]

    used = [i for i in range(len(fixations)) if v1[i+1] < v1[i]] # list of fixations used in this matching
    return v1[len(fixations)], used_word, used

if __name__=='__main__':
    import os
    from predict import load_char_sets

    vid = '../../videos'
    sbjs = [os.path.join(vid,s) for s in os.listdir(vid)]
    sbjs = [s for s in sbjs if os.path.isdir(s)]
    correct = ['computer', 'minimization', 'successfully', 'cognizant']
    for sbj in sbjs:
        trials = [os.path.join(sbj,t) for t in os.listdir(sbj)]
        trials = [t for t in trials if os.path.isdir(t)]
        for trial in trials:
            print 'Levenshtein distances for {f}'.format(f=trial)
            keys_path = os.path.join(trial, 'keys.csv')
            char_sets = load_char_sets(keys_path)
            for word in correct:
                print levenshtein(word, char_sets)
            print
    #print levenshtein('house', [['a','c','x'],['s','h'],['w','o','e','r'],['u','f','d'],['e','s'],['x','q']]) # 1
    #print levenshtein('house', [['a','c','x'],['s','h'],['w','o','e','r','u'],['f','d'],['e','s']]) # 2
    #print levenshtein('house', [['a','c','x'],['z','w'],['w','a','d','r','q'],['f','d'],['v','d']]) # 5
