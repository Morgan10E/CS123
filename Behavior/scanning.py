import behavior
import time
import math

class Behavior(behavior.RobotBehavior):
    def __init__(self, name, robotList, sweep_period, queue):
        super(Behavior, self).__init__(name, robotList)
        self._period = sweep_period
        self._queue = queue
        self._data = [0]*180
        self._averages = [0]*6
        self._landmark_id = [0]*6

    def write_servo_position(self, deg):
        #move the servo motor to deg
        for robot in self._robotList:
            robot.set_port(1, deg)

    def read_psd_distance(self):
        for robot in self._robotList:
            reader = robot.get_port(0)
            return reader
        return 100 #read psd distance

    def get_averages(self):
        angles = [5,20,30,50,60,75,95,110,110,150,155,170]
        for i in range(0,12,2):
            values = self._data[angles[i]:angles[i+1]]
            values.sort()
            leaveOff = 2
            self._averages[i/2] = sum(values[leaveOff:len(values)-leaveOff-1])/(angles[i+1] - angles[i] - 2*leaveOff)
        print self._averages

    def set_landmark_id(self):
        self.get_averages()
        averageID = [0]*6
        jumpID = [0]*6
        if self._averages[0] < 100 and self._averages[0] > 30:
            averageID[0] = 1
        if self._averages[5] < 100 and self._averages[5] > 30:
            averageID[5] = 1
        if self._averages[1] < 160 and self._averages[1] > 30:
            averageID[1] = 1
        if self._averages[4] < 160 and self._averages[4] > 30:
            averageID[4] = 1
        if self._averages[2] < 175 and self._averages[2] > 30:
            averageID[2] = 1
        if self._averages[3] < 175 and self._averages[3] > 30:
            averageID[3] = 1
        print averageID


    def behavior_loop(self):
        print self._name, "behavior_loop() starts!"
        dir = 1
        delta = 1
        deg = 0
        line_psd = {}
        for i in range(0, 181):
            line_psd[i] = None
        period = self._period/len(line_psd)*delta
        print "scanning period: 180deg:",period, "sec"
        while (not self._bQuit):
            for robot in self._robotList:
                robot.set_io_mode(0,0)
                robot.set_io_mode(1,8)
                #print self._name, "behavior_loop(): time = ", time.time(), "sec"

                #move to the desired position: {deg| 0 < deg <=180}
                deg = deg + dir * delta
                offset = 0
                if deg < 0:
                    deg = 0
                    dir = 1
                elif deg > 180 - offset:
                    deg = 0
                    self.write_servo_position(deg)
                    time.sleep(1)
                self.write_servo_position(deg) #implement

                #read the psd distance value
                deg2 = deg
                if (dir == -1):
                    deg2 = deg + offset
                rad = deg2 * math.pi / 180.0
                psd_value = self.read_psd_distance() #implement
                mag = 255 - psd_value;

                #draw graphics
                elem = {}
                elem[0] = mag
                elem[1] = rad
                elem[2] = deg2
                self._queue.put(elem)

                self._data[deg-1] = mag
                self.set_landmark_id()

                #analyze the sensor data[1 ... 180]

            time.sleep(period)
        print self._name, "behavior_loop() finished!"
