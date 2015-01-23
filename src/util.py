import os
import numpy as np

from gaze_data import GazeData, Fixation

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

