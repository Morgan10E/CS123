import Queue
import math

class RobotDraw(object):
    def __init__(self, frame, tk):
        self._frame = frame
        self._points = [36, 40, 600, 400, 20]
        self._canvas = tk.Canvas(frame)
        self._queue = Queue.Queue()
        self._line_l = None
        self._line_r = None
        self._line_psd = {}
        for i in range(0, 181):
            self._line_psd[i] = None

        self.draw_workspace(tk)
        tk.Button(frame, text="Quit", command=quit).pack()

    def start(self):
        self.callback_draw()

    def get_queue(self):
        return self._queue

    def draw_workspace(self, tk):
        pts = self._points
        rect = self._canvas.create_rectangle((pts[2]-pts[0])/2, pts[3]-pts[1], (pts[2]+pts[0])/2, pts[3], outline="red", fill="green", width=2)
        arc_outter = self._canvas.create_arc(pts[2]/2-255-pts[4], pts[3]-pts[1]-255, pts[2]/2+255+pts[4], pts[3]-pts[1]+2*pts[4]+255, start=0, extent=180, outline='red', width=1)
        arc_inner = self._canvas.create_arc((pts[2])/2-pts[4], pts[3]-pts[1], (pts[2])/2+pts[4], pts[3]-pts[1]+2*pts[4], start=0, extent=180, outline='red', width=1)
        expected = self._canvas.create_rectangle((pts[2]-pts[0])/2-80, pts[3], (pts[2]+pts[0])/2+80, pts[3]-180)
        self._canvas.pack(fill=tk.BOTH, expand=1)

    def draw_sensors(self):
        pts = self._points
        while not self._queue.empty():
            info = self._queue.get(0)
            if (len(info) == 2):
                if self._line_l != None:
                    self._canvas.delete(self._line_l)
                if self._line_r != None:
                    self._canvas.delete(self._line_r)
                self._line_l = self._canvas.create_line((pts[2]-pts[0])/2, pts[3]-pts[1], (pts[2]-pts[0])/2, pts[3]-pts[1]-info[0], fill="blue", width=2)
                self._line_r = self._canvas.create_line((pts[2]+pts[0])/2, pts[3]-pts[1], (pts[2]+pts[0])/2, pts[3]-pts[1]-info[1], fill="blue", width=2)
            elif (len(info) == 3):
                mag = info[0] + pts[4]
                rad = math.pi - info[1]
                deg = info[2]
                x = (pts[2])/2 - mag * math.cos(rad)
                y = pts[3]-pts[1]+pts[4] - mag * math.sin(rad)
                x0 = pts[2]/2 - pts[4] * math.cos(rad)
                y0 = pts[3]-pts[1]+pts[4] - pts[4] * math.sin(rad)
                if self._line_psd[deg] != None:
                    self._canvas.delete(self._line_psd[deg])
                    self._line_psd[deg] = None
                color = "red"
                if (rad < math.pi/6):
                    color = "purple"
                elif (rad < math.pi/3):
                    color = "blue"
                elif (rad < math.pi/2):
                    color = "green"
                elif (rad < 2*math.pi/3):
                    color = "yellow"
                elif (rad < 5*math.pi/6):
                    color = "orange"
                self._line_psd[deg] = self._canvas.create_line(x0, y0, x, y, width=1, fill=color)

    def callback_draw(self):
        #print "callback_draw()"
        self.draw_sensors()
        self._frame.after(10, self.callback_draw)
