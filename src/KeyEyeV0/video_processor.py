import os
import cv2
import numpy as np

from util import correlate_gaze
from keyboard_detector import ManualKeyboardDetector
from gaze_data import GazeData, detect_fixations
from argparse import Action

class VideoProcessor(object):
    def __init__(self, folder, redetect=False):
        self.video_path     = os.path.join(folder, 'world.avi')
        gaze_positions_path = os.path.join(folder, 'gaze_positions.npy')
        timestamps_path     = os.path.join(folder, 'timestamps.npy')
        self.fix_path       = os.path.join(folder, 'keyboard_fixations.npy')
        self.gaze_path      = os.path.join(folder, 'keyboard_gaze.npy')
        gaze_positions = np.load(gaze_positions_path)
        timestamps     = np.load(timestamps_path)

        # Get frame size
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        height, width = frame.shape[0:2]
        frame_size = np.array((width, height))
        cap.release()

        self.gaze_per_frame = correlate_gaze(gaze_positions, timestamps, frame_size)
        self.detector = ManualKeyboardDetector(os.path.join(folder, 'key_corners.csv'), redetect)

    def process(self, silent):
        kb_gaze_data = []

        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        height, width = frame.shape[0:2]
        frame_size = np.array((width, height))
        frame_idx = 0
        while ret:
            keyboard = self.detector.detect(frame)
            if keyboard is not None:
                for gd in self.gaze_per_frame[frame_idx]:
                    gaze_in_kb = keyboard.point_in_keyboard_coord(gd.point)
                    kb_gaze_data.append(GazeData(gaze_in_kb, gd.timestamp, gd.confidence))
                if not silent:
                    for p in keyboard.corners:
                        cv2.circle(frame, tuple(p), 5, (0,0,255), -1)
                    cv2.imshow('Detected corners', frame)
                    if cv2.waitKey(1) == 27:
                        break
            else: # In the actual implementation it shouldn't quit
                break
            ret, frame = cap.read()
            frame_idx += 1
        cap.release()
        fixations = detect_fixations(kb_gaze_data)
        np.save(self.gaze_path, [g.values() for g in kb_gaze_data])
        np.save(self.fix_path, [f.values() for f in fixations])
        cv2.destroyAllWindows()

if __name__=='__main__':
    import argparse
    from util import list_trial_folders

    parser = argparse.ArgumentParser(description='Generates ideal paths for given list of words.')
    parser.add_argument('folders', metavar='FOLDER', nargs='*',
                        help='trial folder(s) containing videos to be processed')
    parser.add_argument('-r', '--redetect', action='store_true',
                        help='redetect keyboard corners')
    parser.add_argument('-s', '--silent', action='store_true',
                        help='hide videos')
    args = parser.parse_args()

    folders = args.folders
    if not folders:
        folders = list_trial_folders('../videos')
    for folder in folders:
        print 'Processing {f}...'.format(f=folder)
        VideoProcessor(folder, args.redetect).process(args.silent)
