#train_classifier.py v0.1
#--------------------------
#train a path classifier by synthetically generating paths based
#   on (x,y) character locations of the different layouts and
#   test classifier on real user paths

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imread, imresize
from sklearn.ensemble import RandomForestClassifier
from sklearn import cross_validation


def read_key_coordinates(layout):
    '''reads the x-y coordinates of character locations
    arg: layout - specifies which of the 4 layouts 
        ('dr','sr','p','q')
    ret: dictionary of characters with their corresponding (x,y)'''
    
    #read raw x,y coordinates of all layouts
    df = pd.read_csv("../layout/key_coordinates.csv")
    character_xy = dict()
    arg_list = ['dr','sr','p','q']
    if not(layout in arg_list):
        return character_xy
    
    #construct a dictionary where the alphabets are the keys and 
    #   a normalized x,y tuples are the values
    width = 11
    height = 8.5
    if layout == 'dr':
        character_xy = dict(zip(df.Character, zip(df.drX/width, df.drY/height)))
    if layout == 'sr':
        character_xy = dict(zip(df.Character, zip(df.srX/width, df.srY/height)))
    if layout == 'p':
        character_xy = dict(zip(df.Character, zip(df.pX/width, df.pY/height)))
    if layout == 'q':
        character_xy = dict(zip(df.Character, zip(df.qX/width, df.qY/height)))
        
    return character_xy

    
def read_word_list(filename):
    '''reads wordlist from a file and returns a list of the words
    arg: filename - name of file
    ret: list of words in the file'''
    
    #read words from file (strip newline character at the end of line)
    fn = open(filename)
    word_list = [line.rstrip('\n') for line in fn]
    
    return word_list

    
def generate_path(word, layout):
    '''generates a synthetic path for a given word and layout
    arg: word - word for which to generate path
        layout - layout from which to generate path
    ret: np array of x,y coordinates of the path'''
    
    #initialize path
    path = []
    #size of the keys
    klx = 0.8/11
    kly = 0.8/8.5
    
    #threshold (controls the radius of the distribution of the fixations)
    t = 0.6
    
    #read xy coordinate dict for the layout
    layout_dict = read_key_coordinates(layout)
    
    px = 0
    py = 0
    #for each character in the word
    for char in word:
        x,y = layout_dict[char.upper()]
        path.append((x,y))
        #generate 5-20 random samples centered around the key (fixations)
        rfix = (int)(np.random.uniform(5,20))
        for i in range(rfix):
            fx = np.random.uniform(x-(t*klx),x+(t*klx))
            fy = np.random.uniform(y-(t*kly),y+(t*kly))
            path.append((fx,fy))
        #generate 5-20 times the distance between two contiguous keys points (saccades)
        if not(px==0 and py==0):
            rsac = np.random.uniform(5,20)
            dist = np.linalg.norm(np.asarray([x,y])-np.asarray([px,py]))
            numsac = (int)(rsac*dist)
            xsac = np.linspace(px, x, numsac, endpoint=False)
            ysac = np.linspace(py, y, numsac, endpoint=False)
            xysac = zip(xsac, ysac)
            path.extend(xysac)
            
        px = x
        py = y
        
    return np.asarray(path)
        

    
def visualize_path(coordinates, layout):
    '''visualizes word as a scatterplot
    arg: coordinates - np array containing xy coordinates of the word
         layout - specifies which of the 4 layouts 
        ('dr','sr','p','q')'''
    
    if layout == 'dr':
        im = imread("../layout/DoubleRing.png")
    if layout == 'sr':
        im = imread("../layout/SingleRing.png")
    if layout == 'p':
        im = imread("../layout/SquaredPhone.png")
    if layout == 'q':
        im = imread("../layout/QWERTY.png")
    im = imresize(im,(1000,1000))
    x = coordinates[:,0]*1000
    y = coordinates[:,1]*1000
    plt.figure(figsize=(8,8))
    plt.scatter(x,y)
    plt.imshow(im)
    plt.show()
    
        
def import_recorded_words(dirpath):
    '''import csv of recorded word inside a directory.
    arg: dirpath - directory path containing the csv files
    ret: coord_xy - dictionary where keys are words and np array of
                of xy coordinates are vales'''
    
    coord_xy = dict()
    for subdir, dirs, files in os.walk(dirpath):
        for f in files:
            filename = dirpath+f
            #check if csv file
            if (filename[-3:] == 'csv'):
                df = pd.read_csv(filename)
                #get smoothed x,y coordinates for the filename
                xy = np.asarray(zip(df.smoothed_x, df.smoothed_y))
                #get word value by removing the numeric characters and
                #   .csv file extension
                word = ''.join(i for i in f if not i.isdigit())
                word = word[:-4]
                coord_xy[word] = xy
    return coord_xy
    

def compute_features(path):
    '''takes in a list of xy coordinates corresponding to the word path
    and computes a normalized 2d histogram.
    arg: path - path of xy coordinates of the word
    ret: feat_vect - normalized 2d histogram to be used as a feature vector'''
    
    hist, xe, ye = np.histogram2d(path[:,0], path[:,1], 10, [[0,1],[0,1]], normed=True)
    feat_vect = hist.flatten()
    return feat_vect


def calculate_accuracy(Y_test, Y_pred):
    '''computes the percentage of predictions that match the ground truth
    arg: Y_test: ground truth labels
         Y_pred: predictions made by classifier
    ret: accuracy: score for accuracy'''
    
    sum = 0.0
    for i in range(len(Y_test)):
        if (Y_test[i] == Y_pred[i]):
		sum += 1

    accuracy = sum/len(Y_test)
    return accuracy
    

if  __name__ == "__main__":
    
    #read list of words
    word_list = read_word_list("../data/100words.txt")
    word_list = word_list[0:49]
    #DoubleRing Eyetracker
    dre_X_train = []
    dre_Y_train = []
    #for word in wordlist
    for word in word_list:
        #generate 20 samples for each word
        for i in range(20):
            path =  generate_path(word,'dr')
            feat = compute_features(path)
            dre_X_train.append(feat)
            dre_Y_train.append(word)
    clf = RandomForestClassifier(n_estimators = 100)
    clf = clf.fit(dre_X_train, dre_Y_train)
    
    dre_X_test = []
    dre_Y_test = []
#    ajjen_dict = import_recorded_words("../data/recordings/Ajjen/gaze/DoubleRing/")
#    for word, path in ajjen_dict.iteritems():
#        feat = compute_features(path)
#        dre_X_test.append(feat)
#        dre_Y_test.append(word)
         
    andrew_dict = import_recorded_words("../data/recordings/Andrew/gaze/DoubleRing/")
    for word, path in andrew_dict.iteritems():
        feat = compute_features(path)
        dre_X_test.append(feat)
        dre_Y_test.append(word)
        
#    wenxin_dict = import_recorded_words("../data/recordings/Wenxin/gaze/DoubleRing/")
#    for word, path in wenxin_dict.iteritems():
#        feat = compute_features(path)
#        dre_X_test.append(feat)
#        dre_Y_test.append(word)
    
    dre_Y_pred = clf.predict(dre_X_test)
    accuracy = calculate_accuracy(dre_Y_test, dre_Y_pred)  

    
        
        
        
        
        
    
    
    
         
