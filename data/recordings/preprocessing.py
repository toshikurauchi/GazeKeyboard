import os
import csv

SIZE = 60;
NAME = 'P05';
TYPE = 'mouse';

def process_data(root_dir):
    print root_dir
    results = list()

    output_file = open(NAME + '_results_' + TYPE + '.csv', 'wb')
    writer = csv.writer(output_file)
    
    list_dirs = os.walk(root_dir)

    for root, dirs, files in list_dirs:
        if files == []:
            writer.writerow(['', dirs[0], dirs[1], dirs[2]])
            continue
        
        speed = []
        start_time = []
        avg = []
        counter = 0
        sum = 0
        total = 0
        i = 0
        for f in files:
            if f == []:
                continue
            temp = cal_wpm(os.path.join(root, f), f)
            sum += temp
            speed.append(temp)
            counter = counter +1 
            if counter == 20:
                avg.append(sum/counter)
                total += sum
                sum = 0
                counter = 0
                i = i + 1
        speed.append(avg[0])
        speed.append(avg[1])
        speed.append(avg[2])
        speed.append(total/SIZE)
        results.append(speed)

    for i in range(0, SIZE):        
        writer.writerow(['', results[0][i], results[1][i], results[2][i]])
    for i in range(SIZE, SIZE+3): 
        writer.writerow(["AVG"+ str(i - SIZE), results[0][i], results[1][i], results[2][i]])
    i = i + 1
    writer.writerow(["AVG", results[0][i], results[1][i], results[2][i]])    

    output_file.close()


def cal_wpm(path, filename):
    count_letters = len(filename) - 8
    file = open(path)
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
    return 12000 * count_letters/(float(time_t)-float(time_0))
    
    

process_data(os.path.join(os.getcwd(), NAME + '/' + TYPE))

