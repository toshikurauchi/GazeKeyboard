from numpy.linalg import norm
import csv

from keyboard import PrintedKeyboard

if __name__=='__main__':
    keyboard = PrintedKeyboard()
    words = ['from','snowboard','toolkit','violin','arcade','let']

    with open('ideal_path.csv','wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
        for word in words:
            spamwriter.writerow([word])
            dist = 0
            prev = None
            for char in word:
                pos = keyboard.key_center(char)
                if prev is not None:
                    dist += norm(pos-prev)
                spamwriter.writerow([dist, pos[0], pos[1]])
                prev = pos
