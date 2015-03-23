import os
import numpy as np
import csv

from gaze_data import GazeData, Fixation

def list_trial_folders(videos_path):
    sbjs = [os.path.join(videos_path,s) for s in os.listdir(videos_path)]
    sbjs = [s for s in sbjs if os.path.isdir(s)]
    trials = [os.path.join(sbj,t) for sbj in sbjs for t in os.listdir(sbj)]
    return [t for t in trials if os.path.isdir(t)]

def correlate_gaze(gaze_list,timestamps, frame_size):
    '''
    Source: Pupil-labs (https://github.com/pupil-labs/pupil/blob/master/pupil_src/player/player_methods.py)
    gaze_list: gaze x | gaze y | pupil x | pupil y | timestamp
    timestamps timestamps to correlate gaze data to


    this takes a gaze positions list and a timestamps list and makes a new list
    with the length of the number of recorded frames.
    Each slot conains a list that will have 0, 1 or more assosiated gaze postions.
    load gaze information
    '''
    gaze_list = list(gaze_list)
    timestamps = list(timestamps)

    positions_by_frame = [[] for i in timestamps]

    frame_idx = 0
    try:
        data_point = gaze_list.pop(0)
    except:
        print "No gaze positons in this recording."
        return positions_by_frame

    gaze_timestamp = data_point[4]

    while gaze_list:
        # if the current gaze point is before the mean of the current world frame timestamp and the next worldframe timestamp
        try:
            t_between_frames = ( timestamps[frame_idx]+timestamps[frame_idx+1] ) / 2.
        except IndexError:
            break
        if gaze_timestamp <= t_between_frames:
            gaze_point = np.array(data_point[0:2])
            gaze_point[1] = 1 - gaze_point[1]
            gaze_point *= frame_size
            data = GazeData(gaze_point, data_point[4], data_point[5])
            positions_by_frame[frame_idx].append(data)
            data_point = gaze_list.pop(0)
            gaze_timestamp = data_point[4]
        else:
            frame_idx+=1

    return positions_by_frame

from video_processor import VideoProcessor

def load_or_detect_fixations(folder, redetect=0):
    fixations_path = os.path.join(folder, 'keyboard_fixations.npy')
    if not os.path.isfile(fixations_path):
        VideoProcessor(folder, redetect).process()
    v = np.load(fixations_path)
    return [Fixation.from_values(v[i]) for i in range(v.shape[0])]

def load_char_sets(keys_path):
    with open(keys_path, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        cur_id = -1
        char_sets = []
        for row in spamreader:
            new_id, char, weight, time, pos = int(row[0]), row[1], float(row[2]), float(row[3]), (float(row[4]), float(row[5]))
            if new_id == cur_id:
                cur_char_set[char] = weight
            else:
                cur_id = new_id
                cur_char_set = {char:weight,'_t':time,'_p':pos}
                char_sets.append(cur_char_set)
    return char_sets
