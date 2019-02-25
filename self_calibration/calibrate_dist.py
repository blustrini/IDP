'''
The task the is currently being performed. This will be the most high-level class, so the task must be high-level

N.B. This Task is defined specifically to perform a Calibration task.

Task object should be rewritten generally and class inheritance can be used to perform different tasks.
'''
import time
from task import *

class Calibrate_Dist(Task):
    def __init__(self,Dim):
        #initialise super object
        super().__init__(Dim)
        #name
        self.name = 'Calibrate_Dist'

        #dictionaries represent reaction to trigger based on current state
        self.switch_front = {
        0 : (('b'),1),          #move backward, goto state 1
        1 : ((),1),             #ignore, stay in state 1
        2 : (('s','b'),3),      #stop, then move backward, goto state 3
        3 : ((),3),             #ignore, stay in state 3
        4 : (('s'),0) }         #stop, goto idle

        self.switch_back = {
        0 : (('b'),1),          #move backward, goto state 1
        1 : (('s','f'),2),      #stop, move forward, goto state 2
        2 : ((),2),             #ignore, stay in state 2
        3 : (('s'),4),      #stop, move forward, goto state 4
        4 : ((),4) }            #ignore, stay in state 4

        #processing actions
        self.processes = {
        '12' : (self.start_timer),
        '23' : (self.end_timer,self.start_timer),
        '34' : (self.end_timer,self.calibrate,self.test_calibrate),#calc calibration
        '40' : (self.print_calibration_data)
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back}

    #print calibration data
    def print_calibration_data(self):
        print(self.calibrated_speed)
        return 1
    
    #use timing data to calibrate
    def calibrate(self):
        print('calibration started')
        av_time = sum(self.time_list)/len(self.time_list)
        print(av_time)
        speed = (self.Dim.arena_length - self.Dim.robot_length) / av_time
        self.Dim.speed = speed
        print('calibration ended, result: {}'.format(speed))
        return 1

    def test_calibrate(self):
        #start,wait,func
        self.output.append(self.action_dict['f'])
        print('testing calibration, going forward 40')
        time1 = time.time()
        wait = 40/self.Dim.speed
        func = self.action_dict['s']
        tuple = (time1,wait,func)
        print(tuple)
        self.clock_list.append(tuple)
        return 1
    
