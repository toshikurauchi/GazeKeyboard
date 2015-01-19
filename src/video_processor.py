import os
import cv2
import numpy as np

from util import correlate_gaze
from keyboard_detector import ManualKeyboardDetector
from gaze_data import GazeData, detect_fixations

class VideoProcessor(object):
    def __init__(self, folder):
        self.video_path     = os.path.join(folder, 'world.avi')
        gaze_positions_path = os.path.join(folder, 'gaze_positions.npy')
        timestamps_path     = os.path.join(folder, 'timestamps.npy')
        self.out_path       = os.path.join(folder, 'keyboard_fixations.npy')
        gaze_positions = np.load(gaze_positions_path)
        timestamps     = np.load(timestamps_path)

        # Get frame size
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        height, width = frame.shape[0:2]
        frame_size = np.array((width, height))
        cap.release()

        self.gaze_per_frame = correlate_gaze(gaze_positions, timestamps, frame_size)
        self.detector = ManualKeyboardDetector()

    def process(self):
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
                    gaze_in_kb = np.int0(keyboard.point_in_keyboard_coord(gd.point))
                    kb_gaze_data.append(GazeData(gaze_in_kb, gd.timestamp, gd.confidence))
            else: # In the actual implementation it shouldn't quit
                break
            ret, frame = cap.read()
            frame_idx += 1
        cap.release()
        fixations = detect_fixations(kb_gaze_data)
        np.save(self.out_path, [f.values() for f in fixations])
        cv2.destroyAllWindows()

if __name__=='__main__':
    import sys

    if len(sys.argv) < 2:
        print "USAGE: {p} TRIAL_FOLDER".format(p=sys.argv[0])
        sys.exit()

    folder = sys.argv[1]
    VideoProcessor(folder).process()