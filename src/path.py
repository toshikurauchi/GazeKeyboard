import math
import numpy as np

class Path():

	def __init__(self, word, fixations):
		self.word = word
		self.fixations = fixations

	def gen_path(self, length = 100, random = False):
		'''returns a list of [x, y] coordinates (of certain length) of path, where the number of samples between two
			fixations is proportional to time taken between the two fixations'''
		samples = []
		x_list = []
		y_list = []
		div = float(self.fixations[len(self.fixations)-1][0])/length
		for i in range(1, len(self.fixations)):
			n = int((float(self.fixations[i][0]) - float(self.fixations[i-1][0]))/div)
			x1 = float(self.fixations[i-1][1])
			x2 = float(self.fixations[i][1])
			y1 = float(self.fixations[i-1][2])
			y2 = float(self.fixations[i][2])
			if random:
				x1 = x1 + np.random.randint(-12,13)
				x2 = x2 + np.random.randint(-12,13)
				y1 = y1 + np.random.randint(-12,13)
				y2 = y2 + np.random.randint(-12,13)
			x = np.linspace(x1, x2, n, endpoint = False)
			y = np.linspace(y1, y2, n, endpoint = False)
			x_list.append(x.tolist())
			y_list.append(y.tolist())
		x_list = [item for sublist in x_list for item in sublist]
		y_list = [item for sublist in y_list for item in sublist]
		xf = float(self.fixations[-1][1])
		yf = float(self.fixations[-1][2])
		if random:
			xf = xf + np.random.randint(-12,13)
			yf = yf + np.random.randint(-12,13)
		x_list.append(xf)
		y_list.append(yf)
		samples = [[x, y] for x, y in zip(x_list, y_list)]
		return samples

