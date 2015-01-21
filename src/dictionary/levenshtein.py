# Source: http://en.wikipedia.org/wiki/Levenshtein_distance

def levenshtein(word, buckets, last_dist=0, v0=None, v1=None):
    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty word
    # the distance is always zero as the deletion of a bucket has cost 0
    # (IMPORTANT: this is different from the lenveshtein distance!)
    if v0 is None:
        v0 = [0]*(len(buckets)+1)
    if v1 is None:
        v1 = list(v0)
    if len(word) == 0:
        return v0[len(buckets)], last_dist

    # calculate v1 (current row distances) from the previous row v0
    # first element of v1 is A[i+1][0]
    #   edit distance is delete (i+1) chars in word to match empty bucket list
    #   cost of deleting char in word is 1
    v1[0] = v0[0] + 1

    # use formula to fill in the rest of the row
    for i in range(len(buckets)):
        cost = 0 if word[0] in buckets[i].keys() else 1
        # IMPORTANT: the following line is different from the levenshtein
        # distance. We don't penalize deletions from buckets list.
        v1[i + 1] = min([v1[i], v0[i + 1] + 1, v0[i] + cost])

    last_dist = v1[-1]
    if len(word) == 1: # To avoid an unnecessary function call
        return v1[len(buckets)], last_dist
    return levenshtein(word[1:], buckets, last_dist, v1, v0)

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
                dist, last_dist = levenshtein(word, char_sets)
                print word, dist
            print
