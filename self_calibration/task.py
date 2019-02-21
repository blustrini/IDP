'''
The task the is currently being performed. This will be the most high-level class, so the task must be high-level

N.B. This Task is defined specifically to perform a Calibration task.

Task object should be rewritten generally and class inheritance can be used to perform different tasks.
'''
import time
from dim import *

class Task():
    def __init__(self):
        '''
        flowchart
                  0         1          2           3            4
        states: idle, align_back, goto_front, goto_back, calibration_test
        '''
        #initialise output
        self.output = []
        #initialise dimension object
        self.Dim = Dim()
        #current state
        self.state = 0

        self.action_dict = {
        'f' : 1,
        'b' : 2,
        's' : 5
        }

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

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        'sf': self.switch_front,
        'sb': self.switch_back}

        #all processes to be carried out on state switches
        self.processes = {
        #maps state switch to process
        }

        #output
        self.output = []

        #processing actions
        self.processes = {
        '12' : (self.start_timer),
        '23' : (self.end_timer,self.start_timer),
        '34' : (self.end_timer,self.calibrate,self.test_calibrate),#calc calibration
        '40' : (self.print_calibration_data),
        '22' : (self.drive) #test, remove this
        }

        #processing functions -----------------------

        #initialise time saving attributes
        self.time = 0
        self.time_list = []
        #initialise calibration value
        self.calibrated_speed = 1

        #initialise clock_list
        self.clock_list = []



    #get list of instructions, in the given order
    def get_instructions(self,data):
        #initialise list
        print('begin getting instructions')
        list = []
        #get instructions corresponding to each item in list
        for i in data[0]:
            list.append(self.action_dict[i])
            print('key {} found in action dict'.format(i))
        #change state
        self.change_state(data[1])
        #return list of instructions ready for writing on serial
        self.output += list

    #change state and perform any functions associated with change of state
    def change_state(self,next_state):
        #create the key for the processes dictionary
        key = str(self.state)+str(next_state)
        #call the relevant processes
        try:
            for function in self.processes[key]:
                print('{} found in processes dict'.format(function))
                function()
            #update state
            print('state changed {}:{}'.format(self.state,next_state))
        except TypeError:
            func = self.processes[key]
            print('{} found in processes dict'.format(func))
            func()
        except KeyError:
            print('{} not in process dict'.format(key))
        self.state = next_state

        return 1

    #start a timer
    def start_timer(self):
        print('timer start')
        self.time = time.time()
        return 1

    #end timer
    def end_timer(self):
        end_time = time.time()
        self.time_list.append(end_time-self.time)
        self.time = 0
        print('timer end')
        return 1

    #print calibration data
    def print_calibration_data(self):
        print(self.calibrated_speed)
        return 1
    
    #use timing data to calibrate
    def calibrate(self):
        print('calibration started')
        av_time = sum(self.time_list)/len(self.time_list)
        speed = (self.Dim.arena_length - self.Dim.robot_length) / av_time
        self.calibrated_speed = speed
        print('calibration ended')
        return 1

    def test_calibrate(self):
        #start,wait,func
        self.output.append(self.action_dict['f'])
        print('testing calibration, going forward 40')
        time1 = time.time()
        wait = 40*self.calibrated_speed
        func = self.action_dict['s']
        tuple = (time1,wait,func)
        self.clock_list.append(tuple)
        return 1


    def update(self):
        time1 = time.time()
        for item in self.clock_list:
            if time-item[0] >= item[1]:
                for func in item[2]:
                    self.output.append(func)
                self.clock_list.remove(item)

    def drive(self):
        self.output.append(1)
        
            


    
