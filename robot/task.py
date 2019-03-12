'''
The task the is currently being performed. This will be the most high-level class, so the task must be high-level

N.B. This Task is defined specifically to perform a Calibration task.

Task object should be rewritten generally and class inheritance can be used to perform different tasks.
'''
import time
from dim import *

class Task():
    def __init__(self,Dim):

        self.name = 'Name'

        self.active = 0
        #initialise output
        self.output = []
        #initialise dimension object
        self.Dim = Dim
        #current state
        self.state = 0
        #output
        self.output = []
        self.action_dict = {
        'f' : b'\x01',
        'b' : b'\x02',
        'L' : b'\x03', #pivot left
        'R' : b'\x04', #pivot right
        's' : b'\x05',
        'l' : b'\x06', #soft turn left
        'r' : b'\x07', #soft turn right
        #'p_l' : b'\x08', #pid left
        #'p_r' : b'\x09', #pid right
        #'h' : b'\x10', #halt everything
        #'H' : b'\x11', #resume
        'A' : b'\x08', #flip switch accept
        'E' : b'\x09', #flip switch eject
        'B' : b'\x10', # flip switch block
        #'d' : b'\x15', #drive diagonally right
        #'p_s' : b'\x16', #pid stop
        #'w_r' : b'\x17', #rotate pickup wheel
        #'w_s' : b'\x18', #start pickup wheel
        'O' : b'\x12' #drop blocks onto plaform
        }
        #initialise time saving attributes
        self.time = 0
        self.time_list = []
        #initialise clock_list (init,wait,function)
        self.clock_list = []
        #initialise task_control (task_name,on/off,reset)
        self.task_control = []

    #get list of instructions, in the given order
    def get_instructions(self,data):
        #initialise list
        #print('begin getting instructions')
        list = []
        #get instructions corresponding to each item in list
        for i in data[0]:
            list.append(self.action_dict[i])
            print('key {} found in action dict'.format(i))
        #return list of instructions ready for writing on serial
        self.output += list
        #change state
        self.change_state(data[1])

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
        except TypeError:
            func = self.processes[key]
            func()
        except KeyError:
            pass
            #print('{} not in process dict'.format(key))
        print(self.name + ' state changed {}:{}'.format(self.state,next_state))            
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

    def update(self):
        time1 = time.time()
        for item in self.clock_list:
            if time1-item[0] >= item[1]:
                print('triggered')
                try:
                    for func in item[2]:
                        if 'y' in str(type(func)):
                            self.output.append(func)
                        else:
                            func()
                except TypeError:
                    func = item[2]
                    if 'y' in str(type(func)):
                        self.output.append(func)
                    else:
                        func()
                self.clock_list.remove(item)  

    def activate(self,on,reset=True):
        if reset:
            self.state = 0
            self.clock_list = []
        if on:
            self.active = 1
            print('{} activated into state {}'.format(self.name,self.state))
        else:
            self.active = 0
            print('{} deactivated'.format(self.name))
     


    
