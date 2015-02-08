"""
Stream Pupil gaze coordinate data using zmq to control a mouse with your eye. 
Please note that marker tracking must be enabled, and in this example we have named the surface "screen." 
You can name the surface what you like in Pupil capture and then write the name of the surface you'd like to use on line 17. 
"""
import zmq

#network setup
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5000")
#filter by messages by stating string 'STRING'. '' receives all messages
socket.setsockopt(zmq.SUBSCRIBE, '')
smooth_x, smooth_y= 0.5, 0.5

def get_data(resolution, surface_name='keyboard', smooth=True, max_it=10):
    global smooth_x, smooth_y
    x_dim, y_dim = resolution[0], resolution[1]
    x, y = None, None
    count = 0
    while x is None and count < max_it:
        count += 1
        msg = socket.recv()
        items = msg.split("\n") 
        msg_type = items.pop(0)
        items = dict([i.split(':') for i in items[:-1] ])    
        if msg_type == 'Pupil':
            try:
                gaze_on_keyboard = items["realtime gaze on "+surface_name]
                raw_x,raw_y = map(float,gaze_on_keyboard[1:-1].split(','))
            
                x, y = raw_x, raw_y
                if smooth:
                    # smoothing out the gaze so the mouse has smoother movement
                    smooth_x += 0.5 * (raw_x-smooth_x)
                    smooth_y += 0.5 * (raw_y-smooth_y)

                    x = smooth_x
                    y = smooth_y

                y = 1-y # inverting y so it shows up correctly on screen
                x *= x_dim
                y *= y_dim
            except KeyError:
                return None
            if x is not None:
                return [x,y]
    return None

if __name__=='__main__':
    for i in range(60):
        print get_data((640,480), smooth=False)