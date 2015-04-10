import numpy as np
import os
import cv2
from numpy.linalg import norm
import pickle
import math
import csv

from keyboard import PrintedKeyboard
from pupil_client import get_data
from gaze_data import detect_fixations
from classify_paths import generate_vector

class ScanpathPlotter(object):
    def __init__(self, keyboard):
        self.max_fix_rad = 50
        self.fix_color   = (0, 0, 255)
        self.gaze_color  = (255, 0, 0)
        self.sac_color   = (0, 255, 0)
        self.data        = []
        self.fixations   = []
        self.start_idx   = 0
        self.keyboard    = keyboard
        self.radius      = 5
        self.max_length  = 10
        self.max_fixations = 5
        self.classifier  = pickle.load(open('RF.p', 'rb'))
        self.word_fix    = []
        self.words       = ''

        #if unfiltered:
        #    gaze = np.load(os.path.join(folder, 'keyboard_gaze.npy'))[:,0:1]
        #    self.data = [[g[0][0], g[0][1], 1] for g in gaze]
        #    self.max_fix_rad = 5
        #else:
        #    max_duration = np.max([f.duration for f in fixations])
        #    self.data = [[f.pos[0], f.pos[1], float(f.duration)/max_duration] for f in fixations]
    
    def gen_path(self, fixations, length = 100, random = False):
        '''returns a list of [x, y] coordinates (of certain length) of path, where the number of samples between two
            fixations is proportional to time taken between the two fixations'''
        if len(fixations) < 3 or fixations[-1][0] == 0:
            return None
        print 'fix', len(fixations)
        samples = []
        x_list = []
        y_list = []
        start = fixations[0][0]
        end = fixations[-1][0]
        div = (end-start)/length
        for i in range(1,(len(fixations)-1)):
            n1 = math.floor(fixations[i-1][0]/div)
            n2 = math.floor(fixations[i][0]/div)
            n = n2 - n1
            x1 = fixations[i-1][1]
            x2 = fixations[i][1]
            y1 = fixations[i-1][2]
            y2 = fixations[i][2]
            if random:
                x1 = x1 + np.random.randint(-12,13)
                x2 = x2 + np.random.randint(-12,13)
                y1 = y1 + np.random.randint(-12,13)
                y2 = y2 + np.random.randint(-12,13)
            x = np.linspace(x1, x2, n, endpoint = False)
            y = np.linspace(y1, y2, n, endpoint = False)
            x_list.append(x.tolist())
            y_list.append(y.tolist())
        if (len(fixations) == 2):
            i = 1
            n2 = math.floor(fixations[1][0])
        x1 = fixations[i-1][1]
        x2 = fixations[-1][1]
        y1 = fixations[i-1][2]
        y2 = fixations[-1][2]
        if random:
            x1 = x1 + np.random.randint(-12,13)
            x2 = x2 + np.random.randint(-12,13)
            y1 = y1 + np.random.randint(-12,13)
            y2 = y2 + np.random.randint(-12,13)
        n = length - n2 + start
        x = np.linspace(x1, x2, n, endpoint = True)
        y = np.linspace(y1, y2, n, endpoint = True)
        x_list.append(x.tolist())
        y_list.append(y.tolist())
        x_list = [item for sublist in x_list for item in sublist]
        y_list = [item for sublist in y_list for item in sublist]
        samples = [[x, y] for x, y in zip(x_list, y_list)]
        return samples

    def add_new_fixations(self, new_fixations):
        if not new_fixations:
            return
        if len(self.word_fix) == 0:
            fix = self.keyboard.pix2inch(new_fixations[0])
            self.word_fix.append((0, fix[0], fix[1]))
            new_fixations = new_fixations[1:]
        for i in range(len(new_fixations)):
            fix = self.keyboard.pix2inch(new_fixations[i])
            last_fix = self.word_fix[-1]
            dist = norm(np.array(last_fix[1:3])-fix)
            self.word_fix.append((last_fix[0]+dist, fix[0], fix[1]))

    def plot(self, new_data):
        kb_img = self.keyboard.image()
        if new_data is not None:
            self.data.append(keyboard.inch2pix(new_data[:2]))
            new_fixations, self.start_idx = detect_fixations(self.data, self.start_idx)
            self.fixations.extend(new_fixations)
            self.add_new_fixations(new_fixations)
            if len(self.fixations) > 100:
                self.start_idx = max(self.start_idx - len(self.fixations) + 100, 0)
                self.fixations = self.fixations[-100:]
            if len(self.fixations)>0 and self.keyboard.layout.spacebar.in_key(keyboard.pix2inch(self.fixations[-1])):
                print "SPACE!!!!!"
                path = self.gen_path(self.word_fix)
                count = 0
                word = None
                candidates = []
                most_prob_word = None
                max_prob = 0
                while path and count < 10:
                    probs = self.classifier.predict_proba(generate_vector(path))
                    candidates.append(self.classifier.predict(generate_vector(path))[0])
                    cur_max = max(probs[0])
                    if cur_max > max_prob:
                        max_prob = cur_max
                        most_prob_word = candidates[-1]
                    self.word_fix = self.word_fix[1:]
                    if len(self.word_fix) > 1:
                        self.word_fix = [(f[0]-self.word_fix[0][0], f[1], f[2]) for f in self.word_fix]
                        path = self.gen_path(self.word_fix)
                    count += 1
                print max_prob, most_prob_word, candidates
                if candidates:
                    word = max(set(candidates), key=candidates.count)
                if word:
                    self.words += ' ' + word.upper()
                self.word_fix = []
            #if len(self.fixations) > 2:
                #print 'distance: ', norm(self.fixations[-1]-self.fixations[-2])
        draw_data = self.data[-self.max_length:]
        draw_fixations = self.data[-self.max_fixations:]
        
        cv2.putText(kb_img, self.words, tuple(np.int0(keyboard.inch2pix((15, 10)))), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3, cv2.CV_AA)
        # Draw scanpath
        for i in range(len(draw_fixations)-1):
            pos1 = tuple(np.int0(draw_fixations[i]))
            pos2 = tuple(np.int0(draw_fixations[i+1]))
            cv2.line(kb_img, pos1, pos2, self.sac_color, 5)
        #for d in draw_data:
         #   cv2.circle(kb_img, tuple(np.int0(d[:2])), self.radius, self.gaze_color, -1)
        for f in draw_fixations:
            cv2.circle(kb_img, tuple(np.int0(f)), self.radius, self.fix_color, -1)
        # Resize image to show
        h, w = kb_img.shape[0:2]
        new_w = 1000
        #kb_img = cv2.resize(kb_img, (new_w, new_w*h/w))
        return kb_img

if __name__=='__main__':
    import argparse

    keyboard = PrintedKeyboard()
    keyboard.image()
    resolution = (keyboard.layout.width, keyboard.layout.height)
    plotter = ScanpathPlotter(keyboard)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video = cv2.VideoWriter('video.avi', fourcc, 30, keyboard.size_pix)
    while True:
        gaze = get_data(resolution, smooth=False)
        #print 'gaze', gaze
        img = plotter.plot(gaze)
        video.write(img)
        cv2.imshow('Player', img)
        if cv2.waitKey(1) == 27:
            plotter = ScanpathPlotter(keyboard)
    cv2.destroyAllWindows()
