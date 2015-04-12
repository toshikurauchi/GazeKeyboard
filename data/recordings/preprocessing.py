import os
import csv

size = 50;

def Test1(rootDir):
    L = list();
    
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print "############################################################"
            print d
            print "############################################################"
            temp = list()
            temp.append(d)
            sub_dirs = os.walk(os.path.join(root, d))
            for root1, dirs1, files1 in sub_dirs:
                for f in files1:
                    print os.path.join(root1, f)
                    temp.append(calMT(os.path.join(root1, f)))
            L.append(temp)
            temp = []
    print L;

    results = open('results_mouse.csv', 'wb')
    writer = csv.writer(results)
    for i in range(0, size):        
        writer.writerow([L[0][i], L[1][i], L[2][i], L[3][i]])
    results.close()


def calMT(filename):
    file = open(filename)
    heading = file.readline()
    try:
        data_0 = file.readline()
        fields = data_0.split(',')
        time_0 = fields[0]
        print time_0
        data_t = file.readlines()[-1]
        fields = data_t.split(',')
        time_t = fields[0]
        print time_t
    except IndexError:
        return -1
    file.close()
    return int(time_t)-int(time_0)
    
    



Test1("D:/Git/GazeKeyboard/data/recordings/ajjen/mouse")
