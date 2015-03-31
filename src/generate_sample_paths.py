import csv
from path import Path


if __name__ =='__main__':
	with open('ideal_path.csv', 'rb') as csvfile:
		#read .csv file containing words and their corresponding ideal fixations
		spamreader = csv.reader(csvfile, delimiter=',')
		#populate a separate lists for words, and their corresponding fixations
		word_list = []
		fixations_list = []
		fixations = []
		for row in spamreader:
			if (len(row) == 1):
				if word_list:
					fixations_list.append(fixations)
					fixations = []
				word = row[0]
				word_list.append(word)
			else:
				fixations.append(row)
		fixations_list.append(fixations)

	samples_list = []
	for i in range(len(word_list)):
		p = Path(word_list[i], fixations_list[i])
		samples = p.gen_path(50, True)
		samples_list.append(samples)




