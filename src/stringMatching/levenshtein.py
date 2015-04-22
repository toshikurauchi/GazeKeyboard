import math
import logging

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

    for i in range(len(buckets)):
        bucket = buckets[i]
        for j in range(len(word)):
            # calculate v1 (current row distances) from the previous row v0
            # first element of v1 is A[i+1][0]
            #   edit distance is delete (i+1) chars in word to match empty bucket list
            #   cost of deleting char in word is 1
            char = word[j]
            A[j+1][i+1] = levenshtein_iter(char, bucket, A[j][i], A[j][i+1], A[j+1][i])
    return A[len(word)][len(buckets)]

def levenshtein_iter(char, bucket, A00, A01, A10):
    '''
    Calculates one iteration of the levenshtein algorithm
    for a given character and bucket
    '''
    assert len(char) == 1, 'Single char expected, got string of length {l}'.format(l=len(char))

    match_cost = 0 if char in bucket.keys else 1
    key_pos = bucket.layout.key_pos(char)
    if key_pos is None:
        insert_cost = 1
        logging.error('Layout does not contain this character')
    else:
        dist = math.sqrt((key_pos[0]-bucket.pos[0])**2 + (key_pos[1]-bucket.pos[1])**2)#/bucket.layout.size[0]
        insert_cost = dist
        if match_cost == 0:
            match_cost = dist#/bucket.count
    # IMPORTANT: the following line is different from the levenshtein
    # distance. We don't penalize deletions from buckets list.
    A11 = min([A10, A01 + insert_cost, A00 + match_cost])

    return A11
