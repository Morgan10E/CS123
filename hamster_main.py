'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import signal
import threading
import time
import Tkinter as tk

from HamsterAPI.comm_ble import RobotComm
#from HamsterAPI.comm_usb import RobotComm
import draw
from Behavior import motion, color, sound, proxy, scanning

gFrame = None
gBehaviors = {}

def quit():
    print "quitting..."
    for i in range(0, len(gBehaviors)):
        gBehaviors[i].set_bQuit(True)
    time.sleep(1)
    gFrame.quit()

def clean_up():
    quit()
    print "cleaning up..."

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    clean_up()

signal.signal(signal.SIGINT, signal_handler)

def main(argv=None):
    # instantiate COMM object
    comm = RobotComm(1, -50) #maxRobot = 1, minRSSI = -50
    if comm.start():
        print 'Communication starts'
    else:
        print 'Error: communication'
        return

    # instanciate Robot
    robotList = comm.get_robotList()

    global gFrame
    gFrame = tk.Tk()
    gFrame.geometry('600x500')
    #gFrame.focus_set()
    #gFrame.bind('<KeyPress>', joystick)

    gRobotDraw = draw.RobotDraw(gFrame, tk)

    # create behaviors using set
    global gBehaviors
    gBehaviors = {}
    # gBehaviors[0] = color.Behavior("color", robotList)
    # gBehaviors[1] = sound.Behavior("sound", robotList)
    # gBehaviors[2] = motion.Behavior("motion", robotList, 10)
    # gBehaviors[3] = proxy.Behavior("proxy", robotList, 85, 0.01, gRobotDraw.get_queue())
    gBehaviors[0] = scanning.Behavior("scanning", robotList, 16.0, gRobotDraw.get_queue())

    # start behavior threads using list
    behavior_threads = []
    for i in range(0, len(gBehaviors)):
        gBehaviors[i].set_bQuit(False)
        behavior_threads.append(threading.Thread(target=gBehaviors[i].behavior_loop, name = gBehaviors[i].get_name()))

    for thread in behavior_threads:
        thread.daemon = True
        thread.start()

    gRobotDraw.start()
    gFrame.mainloop()

    for behavior in behavior_threads:
        print "joining... ", behavior.getName()
        behavior.join()
        print behavior.getName(), "joined!"

    for robot in robotList:
        robot.reset()

    comm.stop()
    comm.join()

    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())
