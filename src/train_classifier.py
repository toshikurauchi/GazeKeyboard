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

    
def generate_path(word, layout, mode):
    '''generates a synthetic path for a given word and layout
    arg: word - word for which to generate path
        layout - layout from which to generate path
        mode - eyegaze or head
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
    
    #generate path for eyegaze
    if mode=='e':
         
        px = 0
        py = 0
        #for each character in the word
        for char in word:
            x,y = layout_dict[char.upper()]
            path.append((x,y))
            #generate 5-20 random samples centered around the key (fixations)
            rfix = (int)(np.random.uniform(5,20))
            #perturb center of key (because fixations are not really centered on the
            #   exact key center)
            cx = np.random.uniform(x-(t*klx/3),x+(t*klx/3))
            cy = np.random.uniform(y-(t*kly/3),y+(t*kly/3))
            for i in range(rfix):
                fx = np.random.uniform(cx-(t*klx),x+(t*klx))
                fy = np.random.uniform(cy-(t*kly),y+(t*kly))
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
    
    #generate path for head
    if mode=='h':
        px = 0
        py = 0
        #for each character in the word
        for char in word:
            x,y = layout_dict[char.upper()]
            #randomly perturb center of key
            cx = np.random.uniform(x-(t*klx/3),x+(t*klx/3))
            cy = np.random.uniform(y-(t*kly/3),y+(t*kly/3))
            path.append((cx,cy))
            #generate 20-25 times the distance between two contiguous keys points
            if not(px==0 and py==0):
                rsac = np.random.uniform(20,25)
                dist = np.linalg.norm(np.asarray([x,y])-np.asarray([px,py]))
                numsac = (int)(rsac*dist)
                xsac = np.linspace(px, cx, numsac, endpoint=False)
                ysac = np.linspace(py, cy, numsac, endpoint=False)
                xysac = zip(xsac, ysac)
                path.extend(xysac)     
            px = cx
            py = cy
#        #TODO: smooth path to mimic gaze behavior
#        p = np.asarray(path)
#        x = p[:,0] 
#        y = p[:,1]
#        xsmooth = np.convolve(x, np.ones((5,))/5)[4:]
#        ysmooth = np.convolve(y, np.ones((5,))/5)[4:]
#        path = list()
#        for i in range(xsmooth.shape[0]):
#            path.append((xsmooth[i], ysmooth[i]))
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
    
        
def import_recorded_words(dirpath, mode):
    '''import csv of recorded word inside a directory.
    arg: dirpath - directory path containing the csv files
         mode - eyegaze or head
    ret: coord_xy - dictionary where keys are words and np array of
                of xy coordinates are vales'''
    
    coord_xy = dict()
    for subdir, dirs, files in os.walk(dirpath):
        for f in files:
            filename = dirpath+f
            #check if csv file
            if (filename[-3:] == 'csv'):
                df = pd.read_csv(filename)
                if (mode == 'e'):
                    #get smoothed x,y coordinates for the filename
                    xy = np.asarray(zip(df.smoothed_x, df.smoothed_y))
                if (mode == 'h'):
                    #get mouse x,y coordinates for the filename
                    xy = np.asarray(zip(df.mouse_x, df.mouse_y))
                #get word value by removing the numeric characters and
                #   .csv file extension
                word = ''.join(i for i in f if not i.isdigit())
                word = word[:-4]
                coord_xy[word] = xy
    return coord_xy
    

def compute_features(path, layout, mode):
    '''takes in a list of xy coordinates corresponding to the word path
    and computes a normalized 2d histogram.
    arg: path - path of xy coordinates of the word
         layout - layout from which to generate path
         mode - eyegaze or head
    ret: feat_vect - normalized 2d histogram to be used as a feature vector'''
    
    feat_vect = np.zeros(26)
    
    #compute feature vector for eyegaze
    if mode=='e':
        character_xy = read_key_coordinates(layout)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        r,c = np.shape(path)
        hist1 = np.zeros(26)
        for i in range(r/3 + 1):
            dist_array = [(path[i][0] - character_xy[alphabet[j]][0])**2 + (path[i][1] - character_xy[alphabet[j]][1])**2 for j in range(len(alphabet))]
            dist_array = np.asarray(dist_array)
            hist1[np.argmin(dist_array)] += 1
        hist2 = np.zeros(26)
        for i in range((r/3)+1,2*(r/3)+1):
            dist_array = [(path[i][0] - character_xy[alphabet[j]][0])**2 + (path[i][1] - character_xy[alphabet[j]][1])**2 for j in range(len(alphabet))]
            dist_array = np.asarray(dist_array)
            hist2[np.argmin(dist_array)] += 1
        hist3 = np.zeros(26)
        for i in range(2*(r/3)+1,r):
            dist_array = [(path[i][0] - character_xy[alphabet[j]][0])**2 + (path[i][1] - character_xy[alphabet[j]][1])**2 for j in range(len(alphabet))]
            dist_array = np.asarray(dist_array)
            hist3[np.argmin(dist_array)] += 1
        hist = np.hstack((hist1, hist2, hist3))
        feat_vect = hist/np.linalg.norm(hist)

    #compute feature vector for head    
    if mode=='h':
        character_xy = read_key_coordinates(layout)
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        r,c = np.shape(path)
        hist1 = np.zeros(26)
        for i in range(r/3 + 1):
            dist_array = [(path[i][0] - character_xy[alphabet[j]][0])**2 + (path[i][1] - character_xy[alphabet[j]][1])**2 for j in range(len(alphabet))]
            dist_array = np.asarray(dist_array)
            hist1[np.argmin(dist_array)] += 1
        hist2 = np.zeros(26)
        for i in range((r/3)+1,2*(r/3)+1):
            dist_array = [(path[i][0] - character_xy[alphabet[j]][0])**2 + (path[i][1] - character_xy[alphabet[j]][1])**2 for j in range(len(alphabet))]
            dist_array = np.asarray(dist_array)
            hist2[np.argmin(dist_array)] += 1
        hist3 = np.zeros(26)
        for i in range(2*(r/3)+1,r):
            dist_array = [(path[i][0] - character_xy[alphabet[j]][0])**2 + (path[i][1] - character_xy[alphabet[j]][1])**2 for j in range(len(alphabet))]
            dist_array = np.asarray(dist_array)
            hist3[np.argmin(dist_array)] += 1
        hist = np.hstack((hist1, hist2, hist3))
        feat_vect = hist/np.linalg.norm(hist)
#        r,c = np.shape(path)
#        hist1 = np.zeros(9)
#        for i in range(1, r/3 + 1):
#            y = path[i][1] - path[i-1][1]
#            x = path[i][0] - path[i-1][0]
#            #slope of pair of adjacent points
#            #   add 180 degrees to make range(0,360)
#            angle = np.absolute(np.arctan2(y,x) * 180/np.pi)
#            hist_idx = (int)((angle%180)/20) - 1
#            hist1[hist_idx] += 1
#        hist2 = np.zeros(9)
#        for i in range((r/3)+1,2*(r/3)+1):
#            y = path[i][1] - path[i-1][1]
#            x = path[i][0] - path[i-1][0]
#            #slope of pair of adjacent points
#            #   add 180 degrees to make range(0,360)
#            angle = np.absolute(np.arctan2(y,x) * 180/np.pi)
#            hist_idx = (int)((angle%180)/20) - 1
#            hist2[hist_idx] += 1
#        hist3 = np.zeros(9)
#        for i in range(2*(r/3)+1,r):
#            y = path[i][1] - path[i-1][1]
#            x = path[i][0] - path[i-1][0]
#            #slope of pair of adjacent points
#            #   add 180 degrees to make range(0,360)
#            angle = np.absolute(np.arctan2(y,x) * 180/np.pi)
#            hist_idx = (int)((angle%180)/20) - 1
#            hist3[hist_idx] += 1
#        hist = np.hstack((hist1, hist2, hist3))
#        feat_vect = hist/np.linalg.norm(hist)

    return feat_vect


def calculate_accuracy(Y_test, Y_pred):
    '''computes the percentage of predictions that match the ground truth
    arg: Y_test - ground truth labels
         Y_pred - predictions made by classifier
    ret: accuracy: score for accuracy'''
    
    sum = 0.0
    for i in range(len(Y_test)):
        if (Y_test[i] == Y_pred[i]):
		sum += 1

    accuracy = sum/len(Y_test)
    return accuracy


def train_rf(word_list, layout, mode):
    '''trains a random forest classifier given the words in the wordlist
    by generating a synthetic dataset
    arg: word_list - list of words on which to train classifier
         layout - type of keyboard layout
         mode - eyegaze or head
    ret: clf - trained rf classifier'''
    #DoubleRing Eyetracker
    X_train = []
    Y_train = []
    #for word in wordlist
    for word in word_list:
        #generate 20 samples for each word
        for i in range(20):
            path =  generate_path(word,layout,mode)
            feat = compute_features(path,layout,mode)
            X_train.append(feat)
            Y_train.append(word)
    
    #train classifier
    clf = RandomForestClassifier(n_estimators = 100)
    clf = clf.fit(X_train, Y_train)
    return clf
    
def test_rf(subject, layout, mode, clf):
    '''tests a trained classifier on a recorded test set
    arg: subject - name of folder containing the subject's recordings
         layout - type of keyboard layout
         mode - eyegaze or head
         clf - trained classifier
    ret: Y_test - array of ground truth values for test data 
         Y_pred - array of predictions for test data specified by function argumnents'''
    
    layouts = ['DoubleRing', 'SingleRing', 'Phone', 'Qwerty']
    if layout == 'dr':
        l = layouts[0]
    if layout == 'sr':
        l = layouts[1]
    if layout == 'p':
        l = layouts[2]
    if layout == 'q':
        l = layouts[3]
        
    modes = ['gaze','mouse']
    if mode == 'e':
        m = modes[0]
    if mode == 'h':
        m = modes[1]
    
    #WARNING: MAKE SURE PATHNAME POINTS TO CORRECT DATA FOLDER!
    pathname = "../data/recordings/" + subject + "/" + m + "/" + l + "/"
     
    X_test = []
    Y_test = []
    rec_words = import_recorded_words(pathname, mode)
    for word, path in rec_words.iteritems():
        feat = compute_features(path, layout, mode)
        X_test.append(feat)
        Y_test.append(word)
        
    return (Y_test, clf.predict(X_test))

if  __name__ == "__main__":
    
    #read list of words
    word_list = read_word_list("../data/100words.txt")
    word_list = word_list[0:49]
    
    #test classifier for various combinations of user, layout and mode
    user_list = ["Ajjen","Andrew","Wenxin"]
    layout_list = ["dr", "sr", "p", "q"]
    mode_list = ["e", "h"]
    
    
    for layout in layout_list:
        for mode in mode_list:
            clf = train_rf(word_list, layout, mode)
            for user in user_list:
                Y_test, Y_pred = test_rf(user, layout, mode, clf)
                accuracy = calculate_accuracy(Y_test, Y_pred)  
                
                print("Accuracy for " + user + " for " + layout + " for " + mode + " is: %f," %(accuracy))
            print
        print
    

    
        
        
        
        
        
    
    
    
         
