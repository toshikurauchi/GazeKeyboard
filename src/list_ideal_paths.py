from numpy.linalg import norm
import csv
import argparse

from keyboard import PrintedKeyboard

parser = argparse.ArgumentParser(description='Generates ideal paths for given list of words.')
parser.add_argument('words', metavar='WORD', nargs='*',
                    help='words to use for path generation')
parser.add_argument('-f', '--file', metavar='FILENAME', nargs='+',
                    help='file containing list of words')
parser.add_argument('-l', '--limit', metavar='N', type=int,
                    help='number of words to use from the list')
parser.add_argument('-o', '--output', metavar='FILENAME',
                    default='ideal_path.csv', help='output csv file')
parser.add_argument('-m', '--minlength', metavar='M', type=int, default=0,
                    help='minimum word length to consider')
args = parser.parse_args()

def read_words(filename, limit, min_length):
    words = []
    with open(filename, 'rb') as file:
        count = 0
        if filename[-4:] == '.csv':
            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            spamreader = csv.reader(file, dialect)
            for row in spamreader:
                if limit and count >= limit: break
                if row and len(row[0]) >= min_length:
                    words.append(row[0]) # We consider that the other values are frequencies, etc
                    count += 1
        else:
            for word in file: # Each word is in a line
                if limit and count >= limit: break
                word = word.strip()
                if len(word) >= min_length:
                    words.append(word)
                    count += 1
    return words

keyboard = PrintedKeyboard()
if len(args.words) == 0 and (args.file is None or len(args.file) == 0):
    words = ['from','snowboard','toolkit','violin','arcade','let']
else:
    words = args.words
    if args.file is not None:
        words.extend([word for f in args.file for word in read_words(f, args.limit, args.minlength)])
words = filter(lambda w: len(w) >= args.minlength, words)
if args.limit and args.limit < len(words): words = words[:args.limit]
print words

with open(args.output,'wb') as csvfile:
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
    print 'Output saved as:', args.output
