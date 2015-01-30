import math

class Key(object):
    def __init__(self, key, top_left, width, height):
        self.key = key
        self.top_left = top_left
        self.center = [top_left[0] + width/2, top_left[1] + height/2]
        self.width = width
        self.height = height
        self.rad = math.sqrt(width**2 + height**2)/2

    def relative_dist(self, point):
        dif = [point[i] - self.center[i] for i in range(2)]
        return math.sqrt(dif[0]**2 + dif[1]**2)/self.rad

class PrintedKeyboardLayout(object):
    def __init__(self):
        self.corners = [(6,24),(130,24),(130,64),(6,64)]
        x0, y0 = 9, 27
        width, height = 10, 10
        dx, dy = 12, 12
        rowdx = 6
        self.keys = [Key('q', (x0+0*dx, y0), width, height),
                     Key('w', (x0+1*dx, y0), width, height),
                     Key('e', (x0+2*dx, y0), width, height),
                     Key('r', (x0+3*dx, y0), width, height),
                     Key('t', (x0+4*dx, y0), width, height),
                     Key('y', (x0+5*dx, y0), width, height),
                     Key('u', (x0+6*dx, y0), width, height),
                     Key('i', (x0+7*dx, y0), width, height),
                     Key('o', (x0+8*dx, y0), width, height),
                     Key('p', (x0+9*dx, y0), width, height),
                     Key('a', (x0+rowdx+0*dx, y0+dy), width, height),
                     Key('s', (x0+rowdx+1*dx, y0+dy), width, height),
                     Key('d', (x0+rowdx+2*dx, y0+dy), width, height),
                     Key('f', (x0+rowdx+3*dx, y0+dy), width, height),
                     Key('g', (x0+rowdx+4*dx, y0+dy), width, height),
                     Key('h', (x0+rowdx+5*dx, y0+dy), width, height),
                     Key('j', (x0+rowdx+6*dx, y0+dy), width, height),
                     Key('k', (x0+rowdx+7*dx, y0+dy), width, height),
                     Key('l', (x0+rowdx+8*dx, y0+dy), width, height),
                     Key('z', (x0+2*rowdx+0*dx, y0+2*dy), width, height),
                     Key('x', (x0+2*rowdx+1*dx, y0+2*dy), width, height),
                     Key('c', (x0+2*rowdx+2*dx, y0+2*dy), width, height),
                     Key('v', (x0+2*rowdx+3*dx, y0+2*dy), width, height),
                     Key('b', (x0+2*rowdx+4*dx, y0+2*dy), width, height),
                     Key('n', (x0+2*rowdx+5*dx, y0+2*dy), width, height),
                     Key('m', (x0+2*rowdx+6*dx, y0+2*dy), width, height)]

    def key_center(self, key):
        for k in self.keys:
            if k.key == key:
                return k.center
        return None