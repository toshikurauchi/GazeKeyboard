import numpy as np
import cv2

def draw_scanpath(img, gaze, color, has_duration=False):
    max_fix_rad = 50

    for i in range(len(gaze)-1):
        pos1 = tuple(np.int0(gaze[i][:2]))
        pos2 = tuple(np.int0(gaze[i+1][:2]))
        cv2.line(img, pos1, pos2, color, 1)
    if has_duration:
        max_duration = np.max(gaze[:][2])
        for g in gaze:
            fix_pos = tuple(np.int0(g[:2]))
            rad = int(g[2]*max_fix_rad/max_duration)
            cv2.circle(img, fix_pos, rad, color, -1)

def detect_fixations(data):
    thresh = 20
    avg_frame_time = np.mean([data[i+1][0]-data[i][0] for i in range(len(data)-1)])
    filtered = [[d[0], d[3], d[4]] for d in data if d[5]] #tstamp, x, y
    fixations = []
    cluster = None
    for d in filtered:
        if cluster is None:
            cluster = [d]
        elif dist2cluster(cluster, d) < thresh:
            cluster.append(d)
        else:
            fixations.append(compute_fix(cluster, avg_frame_time))
            cluster = [d]
    fixations.append(compute_fix(cluster, avg_frame_time))
    return fixations

def cluster_center(cluster):
    return np.mean(cluster, 0)[1:3]

def dist2cluster(cluster, gaze):
    center = cluster_center(cluster)
    return np.linalg.norm(gaze[1:3] - center)

def compute_fix(cluster, frame_time):
    center = cluster_center(cluster)
    duration = cluster[-1][0] - cluster[0][0] + frame_time
    return [center[0], center[1], duration]

if __name__ == "__main__":
    import sys
    import csv

    from keyboard import PrintedKeyboard

    if len(sys.argv) < 2:
        print "USAGE: python %s GAZE_DATA_FILE.csv [KEYBOARD_ID]"%sys.argv[0]
        sys.exit()
    keyboard_id = 0
    if len(sys.argv) > 2:
        keyboard_id = int(sys.argv[2])

    # Define colors
    raw_color = (255, 0, 0)
    fix_color = (0, 255, 0)
    smooth_color = (0, 0, 255)

    # Read file
    filename = sys.argv[1]
    header = None
    data = []
    with open(filename, "rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for line in reader:
            if header is None:
                header = line
            else:
                gd = [int(line[0])]
                gd.extend([float(i) for i in line[1:-1]])
                gd.append(True if int(line[-1]) == 1 else False)
                data.append(gd)

    # Denormalize coordinates
    keyboard_src = "Keyboard2a.png"
    if keyboard_id == 1:
        keyboard_src = "Keyboard-circ.jpg"
    if keyboard_id == 2:
        keyboard_src = "Keyboard-phone-rot.jpg"
    
    kb_orig = cv2.imread(keyboard_src)
    kb_img = kb_orig.copy()
    h, w = kb_img.shape[0:2]
    for d in data:
        d[1] *= w
        d[2] *= h
        d[3] *= w
        d[4] *= h
    raw = [[d[1], d[2]] for d in data if d[5]]
    smooth = [[d[3], d[4]] for d in data if d[5]]
    fixations = detect_fixations(data)

    draw_scanpath(kb_img, raw, raw_color)
    draw_scanpath(kb_img, smooth, smooth_color)
    draw_scanpath(kb_img, fixations, fix_color, has_duration=True)

    # Resize image to show
    new_w = 1000
    new_h = new_w*h/w
    kb_img = cv2.resize(kb_img, (new_w, new_h))
    winname = 'Scanpath: ' + filename[filename.rindex('/')+1:]
    cv2.imshow(winname, kb_img)
    key = cv2.waitKey(0)
    while key != 27:
        kb_img = kb_orig.copy()
        if key == ord('1'):
            draw_scanpath(kb_img, raw, raw_color)
        elif key == ord('2'):
            draw_scanpath(kb_img, smooth, smooth_color)
        elif key == ord('3'):
            draw_scanpath(kb_img, fixations, fix_color)
        elif key == ord('4'):
            draw_scanpath(kb_img, fixations, fix_color, has_duration=True)
        elif key == ord('5'):
            draw_scanpath(kb_img, raw, raw_color)
            draw_scanpath(kb_img, smooth, smooth_color)
            draw_scanpath(kb_img, fixations, fix_color, has_duration=True)
        kb_img = cv2.resize(kb_img, (new_w, new_h))
        cv2.imshow(winname, kb_img)
        key = cv2.waitKey(0)
    cv2.destroyAllWindows()
