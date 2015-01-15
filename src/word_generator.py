import itertools
import enchant
import numpy as np
import csv

def generate_combinations(character_list):

        combinations = itertools.product([True, False], repeat = len(character_list))

        solution_list = []
        fraction = 1.0/2
        for combo in combinations:
                candidate_word = ''
                for i in range(len(combo)):
                        if combo[i]:
                                candidate_word += character_list[i]
                if len(candidate_word) > (len(character_list)*fraction):
                        solution_list.append(candidate_word)

        return solution_list

def viable_words(solution_list):

        solution_list_unique = set()
        for item in solution_list:
                solution_list_unique.add(item)

        solution_list_unique = list(solution_list_unique)
        solution_list_unique = filter(None, solution_list_unique)
        viable_words = []
        d = enchant.Dict("en_US")
        for item in solution_list_unique:
                if d.check(item):
                        viable_words.append(item)

        

        return viable_words

if __name__=='__main__':

        keys = []
        with open('../videos/ajjen/014/keys.csv', 'rb') as csvfile:
                my_data = csv.reader(csvfile, delimiter=',')
                for row in my_data:
                        keys.append(row)

        key_start = 0
        max_key = 0
        max_weight = 0
        key_list = []
        for row in keys:
                if int(row[0]) == key_start:
                        if max_weight < row[2]:
                                max_weight = row[2]
                                max_key = row[1]
                else:
                        key_list.append(max_key)
                        key_start = int(row[0])
                        max_key = 0
                        max_weight = 0
                        if int(row[0]) == key_start:
                                if max_weight < row[2]:
                                        max_weight = row[2]
                                        max_key = row[1]
 
                
        print key_list
        key_list_unique = [key_list[0]]
        for i in range(1,len(key_list)):
                if key_list[i] != key_list[i-1]:
                        key_list_unique.append(key_list[i])
        print key_list_unique
        solution_list = generate_combinations(key_list_unique)
        
        output = viable_words(solution_list)
        print output
