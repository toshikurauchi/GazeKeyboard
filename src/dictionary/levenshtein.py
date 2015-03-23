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

def fill_gaps(word, used, buckets, pos_fun):
    if len(buckets) == 0:
        return used
    u = 0
    prev_bucket = 0
    filled = []
    for i in range(len(word)):
        if u < len(used) and used[u][0] == i:
            filled.append(used[u])
            prev_bucket = used[u][1]
            u += 1
        else:
            min_dist = float('inf')
            idx = None
            next = prev_bucket
            if u < len(used): next = used[u][1]
            for j in range(prev_bucket, next+1):
                pos_char = pos_fun(word[i])
                pos_fix = buckets[j]['_p']
                dist = (pos_char[0]-pos_fix[0])**2 + (pos_char[1]-pos_fix[1])**2
                if dist < min_dist:
                    min_dist = dist
                    idx = (i, j)
            if idx is not None:
                prev_bucket = idx[1]
                filled.append(idx)
    return filled

if __name__=='__main__':
    import os
    import sys,inspect
    currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parentdir = os.path.dirname(currentdir)
    sys.path.insert(0,parentdir)

    from util import load_char_sets
    from keyboard_layout import PrintedKeyboardLayout

    keyboard = PrintedKeyboardLayout()
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
                filled = fill_gaps(word, used, char_sets, keyboard.key_center)
                print word, dist, len(used), len(word)-dist, sum([char_sets[u[1]]['_t'] for u in used]), filled
            print
