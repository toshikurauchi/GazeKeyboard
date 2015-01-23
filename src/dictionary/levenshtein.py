# Source: http://en.wikipedia.org/wiki/Levenshtein_distance

def levenshtein(word, buckets):
    # create two work vectors of integer distances
    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty word
    # the distance is always zero as the deletion of a bucket has cost 0
    # (IMPORTANT: this is different from the lenveshtein distance!)
    A = [[0]*(len(buckets)+1) for i in range(len(word)+1)]
    for i in range(len(word)):
        A[i+1][0] = i+1
    enter_idx = [[] for i in range(len(word))]

    for i in range(len(buckets)):
        bucket = buckets[i]
        for j in range(len(word)):
            # calculate v1 (current row distances) from the previous row v0
            # first element of v1 is A[i+1][0]
            #   edit distance is delete (i+1) chars in word to match empty bucket list
            #   cost of deleting char in word is 1
            char = word[j]
            A[j+1][i+1], me = levenshtein_iter(char, bucket, A[j][i], A[j][i+1], A[j+1][i])
            if me:
                enter_idx[j].append((i, A[j+1][i+1]))
    return A[len(word)][len(buckets)], enter_idx

def levenshtein_iter(char, bucket, A00, A01, A10):
    '''
    Calculates one iteration of the levenshtein algorithm
    for a given character and bucket
    '''
    assert len(char) == 1, 'Single char expected, got string of length {l}'.format(l=len(char))

    cost = 0 if char in bucket.keys() else 1
    # IMPORTANT: the following line is different from the levenshtein
    # distance. We don't penalize deletions from buckets list.
    A11 = min([A10, A01 + 1, A00 + cost])
    may_enter = False
    if A11 < A10 and A11 < A01+1:
        may_enter = True

    return A11, may_enter

def find_used(enter_idx, word_len, dist):
    used = []
    for d in range(word_len-1, -1, -1):
        for i in range(len(enter_idx[d])-1,-1,-1):
            cur_idx = enter_idx[d][i]
            if cur_idx[1] == dist:
                dist += 1
                used.append((d,cur_idx[0]))
                break
        dist -= 1
    return used[::-1]

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
                dist, e_idx = levenshtein(word, char_sets)
                used = find_used(e_idx, len(word), dist)
                print word, dist, len(used), len(word)-dist, sum([char_sets[u[1]][word[u[0]]]['t'] for u in used])
            print
