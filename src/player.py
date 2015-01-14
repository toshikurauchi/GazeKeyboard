import cv2
import numpy as np

from keyboard_detector import ManualKeyboardDetector

class Player(object):
    def __init__(self):
        self.detector = ManualKeyboardDetector()
        
    def play(self, filename, gaze_per_frame):
        gaze_rad = 20
        gaze_color = (0, 0, 255)
        
        cap = cv2.VideoCapture(filename)
        ret, frame = cap.read()
        height, width = frame.shape[0:2]
        frame_size = np.array((width, height))
        frame_idx = 0
        while ret:
            keyboard = self.detector.detect(frame)
            if keyboard is not None:
                kb_img = keyboard.image()
                for gaze in gaze_per_frame[frame_idx]:
                    gaze = np.array(gaze['norm_gaze'])
                    gaze[1] = 1 - gaze[1]
                    gaze *= frame_size
                    gaze_in_kb = np.int0(keyboard.point_in_keyboard_coord(gaze))
                    cv2.circle(kb_img, tuple(gaze_in_kb), gaze_rad, gaze_color, -1)
                # Resize image to show
                h, w = kb_img.shape[0:2]
                new_w = 1000
                kb_img = cv2.resize(kb_img, (new_w, new_w*h/w))
                cv2.imshow('Player', kb_img)
            else: # In the actual implementation it shouldn't quit
                break
            if cv2.waitKey(1) == 27:
                break
            ret, frame = cap.read()
            frame_idx += 1
        cap.release()
        cv2.destroyAllWindows()

def correlate_gaze(gaze_list,timestamps):
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
        logger.warning("No gaze positons in this recording.")
        return positions_by_frame

    gaze_timestamp = data_point[4]

    while gaze_list:
        # if the current gaze point is before the mean of the current world frame timestamp and the next worldframe timestamp
        try:
            t_between_frames = ( timestamps[frame_idx]+timestamps[frame_idx+1] ) / 2.
        except IndexError:
            break
        if gaze_timestamp <= t_between_frames:
            positions_by_frame[frame_idx].append({'norm_gaze':(data_point[0],data_point[1]),'norm_pupil': (data_point[2],data_point[3]), 'timestamp':data_point[4],'confidence':data_point[5]})
            data_point = gaze_list.pop(0)
            gaze_timestamp = data_point[4]
        else:
            frame_idx+=1

    return positions_by_frame

if __name__=='__main__':
    import sys
    import os
    
    if len(sys.argv) < 2:
        print "USAGE: {p} TRIAL_FOLDER".format(p=sys.argv[0])
        sys.exit()
    
    folder = sys.argv[1]
    video_path = os.path.join(folder, 'world.avi')
    gaze_positions_path = os.path.join(folder, 'gaze_positions.npy')
    timestamps_path = os.path.join(folder, 'timestamps.npy')
    gaze_positions = np.load(gaze_positions_path)
    timestamps = np.load(timestamps_path)
    positions_per_frame = correlate_gaze(gaze_positions, timestamps)
    
    print 'Playing {f}'.format(f=video_path)
    Player().play(video_path, positions_per_frame)