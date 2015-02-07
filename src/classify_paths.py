import csv
from path import Path
from sklearn.ensemble import RandomForestClassifier
import pickle

def generate_vector(samples):
	'''for each path represented by samples, generate a vector consisting of a
		list of points [x1,y1,s1,x2,y2,s2,...sn-1,xn,yn], s = slope (s = y2 - y1/x2 - x1)'''
	x = []
	x.append(samples[0][0])
	x.append(samples[0][1])
	for j in range(1,len(samples)):
		xdiff = samples[j][0] - samples[j-1][0]
		ydiff = samples[j][1] - samples[j-1][1]
		if (xdiff == 0):
			xdiff = 0.0001
		slope = ydiff/xdiff
		x.append(slope)
		x.append(samples[j][0]) #x-coordinate
		x.append(samples[j][1]) #y-coordinate
	return x

def create_array_wlabels(word_list, fixations_list, n, flag1, flag2, num_rand_samp):
	'''takes a list of words and corresponding fixations and creates an array of features (X),
		and corresponding labels (Y)'''
	X = []
	Y = []
	for i in range(len(word_list)):
		p = Path(word_list[i], fixations_list[i])
		#generate samples for ideal path
		print i
		samples = p.gen_path()
		x = generate_vector(samples)
		if flag1:
			X.append(x)
			Y.append(p.word)
		#generate samples for noisy path
		if flag2:
			for i in range(num_rand_samp):
				samples = p.gen_path(n,flag2)
				x = generate_vector(samples)
				X.append(x)
				Y.append(p.word)
	return X, Y

def calculate_accuracy(Y_test, Y_pred):
	sum = 0.0
	for i in range(len(Y_test)):
		if (Y_test[i] == Y_pred[i]):
			sum += 1

	accuracy = sum/len(Y_test)
	return accuracy



if __name__ =='__main__':
	with open('ideal_path6.csv', 'rb') as csvfile:
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

	#for each word and its corresponding list of fixations, generate paths (1 ideal and 19 random) 
	#   of constant length and create a training set to train a classifier
	#	training set of each path consists of points [x1,y1,s1,x2,y2,s2,...sn-1,xn,yn]
	#	s = slope (s = y2 - y1/x2 - x1)
	X_train, Y_train = create_array_wlabels(word_list, fixations_list, 100, True, True, 20)

	

	X_test, Y_test = create_array_wlabels(word_list, fixations_list, 100, False, True, 5)

	# #Load test set
	# ajjen_list = ['arcade0', 'arcade1', 'arcade2', 'from0', 'from1', 'from2', 'let0', 'let1', 'let2', 'let3', 'let4', 'snowboard0', 'snowboard1', 'snowboard2', 'toolkit0', 'toolkit1', 'toolkit2', 'violin0', 'violin1', 'violin2']
	# andrew_list = ['arcade0', 'arcade1', 'arcade2', 'arcade3', 'arcade4', 'from0', 'from1', 'from2', 'from3', 'from4', 'from5', 'let0', 'let1', 'let2', 'snowboard0', 'snowboard1', 'snowboard2', 'toolkit0', 'toolkit1', 'toolkit2', 'violin0', 'violin1', 'violin2']
	
	# ajjen_pre = '../videos/ajjen/'
	# andrew_pre = '../videos/andrew/'
	# word_list = []
	# fixations_list = []
	# for name in range(len(ajjen_list)):	
	# 	fname = ajjen_pre + ajjen_list[name] + '/fixations.csv'
	# 	with open(fname, 'rb') as csvfile:
	# 		#read .csv file containing words and their corresponding ideal fixations
	# 		spamreader = csv.reader(csvfile, delimiter=',')
	# 		#populate a separate lists for words, and their corresponding fixations
	# 		fixations = []
	# 		word_list.append(ajjen_list[name][:-1])
	# 		for row in spamreader:
	# 			fixations.append(row)
	# 		#make sure first timestamp is 0, and everything else is relative to 0
	# 		b = float(fixations[0][0])
	# 		for i in range(len(fixations)):
	# 			fixations[i][0] = str(float(fixations[i][0])-b)
	# 	fixations_list.append(fixations)
	# for name in range(len(andrew_list)):
	# 	fname = andrew_pre + andrew_list[name] + '/fixations.csv'
	# 	with open(fname, 'rb') as csvfile:
	# 		spamreader = csv.reader(csvfile, delimiter=',')
	# 		fixations = []
	# 		word_list.append(andrew_list[name][:-1])
	# 		for row in spamreader:
	# 			fixations.append(row)
	# 		#make sure first timestamp is 0, and everything else is relative to 0
	# 		b = float(fixations[0][0])
	# 		for i in range(len(fixations)):
	# 			fixations[i][0] = str(float(fixations[i][0])-b)
	# 	fixations_list.append(fixations)

	# #create a training set to train a classifier
	# X_test, Y_test = create_array_wlabels(word_list, fixations_list, 100, False)
		
	# #Train random forest classifier on training set
	clf = RandomForestClassifier(n_estimators = 100)
	clf = clf.fit(X_train, Y_train)
	pickle.dump(clf,open("RF.p","wb"))
	Y_pred = clf.predict(X_test)

	accuracy = calculate_accuracy(Y_test, Y_pred)

	
						
				



		
		






