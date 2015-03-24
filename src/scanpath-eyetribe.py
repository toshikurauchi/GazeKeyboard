import numpy as np
import sys
import cv2

from keyboard import PrintedKeyboard

if len(sys.argv) < 2:
    print "USAGE: python %s GAZE_DATA_FILE.csv"%sys.argv[0]
    sys.exit()

filename = sys.argv[1]

sac_color = (255, 0, 0)
gaze = np.load(filename)[:,0:1]
data = [[g[0][0], g[0][1]] for g in gaze]

keyboard = PrintedKeyboard()
kb_img = keyboard.image()
h, w = kb_img.shape[0:2]
for d in data:
    d[0] *= w
    d[1] *= h
# Draw scanpath
for i in range(len(data)-1):
    pos1 = tuple(np.int0(data[i]))
    pos2 = tuple(np.int0(data[i+1]))
    cv2.line(kb_img, pos1, pos2, sac_color, 5)
# Resize image to show
new_w = 1000
kb_img = cv2.resize(kb_img, (new_w, new_w*h/w))
cv2.imshow('Scanpath', kb_img)
while cv2.waitKey(0) != 27:
    pass
cv2.destroyAllWindows()