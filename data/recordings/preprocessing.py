import os
import csv

SIZE = 50;
NAME = 'andrew';
TYPE = 'gaze';

def process_data(root_dir):
    print root_dir
    results = list()

    output_file = open(NAME + '_results_' + TYPE + '.csv', 'wb')
    writer = csv.writer(output_file)
    
    list_dirs = os.walk(root_dir)

    for root, dirs, files in list_dirs:
        if files == []:
            writer.writerow([dirs[0], '', dirs[1], '', dirs[2], '', dirs[3]])
            continue
        
        speed = []
        start_time = []
        for f in files:
            if f == []:
                continue
            speed.append(cal_mmt(os.path.join(root, f))[1])
            start_time.append(cal_mmt(os.path.join(root, f))[0])
        results.append(start_time)
        results.append(speed)
        print results

    for i in range(0, SIZE - 1):        
        writer.writerow([results[0][i], results[1][i], results[2][i], results[3][i], results[4][i], results[5][i], results[6][i], results[7][i]])

    output_file.close()


def cal_mmt(filename):
    count_letters = len(filename) - 5
    file = open(filename)
    heading = file.readline()
    try:
        data_0 = file.readline()
        fields = data_0.split(',')
        time_0 = fields[0]
        data_t = file.readlines()[-1]
        fields = data_t.split(',')
        time_t = fields[0]
    except IndexError:
        return [-1, -1]
    file.close()
    return [time_0, (int(time_t)-int(time_0))/count_letters]
    
    



process_data(os.path.join(os.getcwd(), NAME + '/' + TYPE))
