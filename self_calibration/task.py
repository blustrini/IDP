'''
The task the is currently being performed. This will be the most high-level class, so the task must be high-level

N.B. This Task is defined specifically to perform a Calibration task.

Task object should be rewritten generally and class inheritance can be used to perform different tasks.
'''
import time
from dim import *

class Task():
    def __init__(self,Dim):

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
        's' : b'\x05'
        }
        #initialise time saving attributes
        self.time = 0
        self.time_list = []
        #initialise clock_list (init,wait,function)
        self.clock_list = []
        #initialise task_control (task_name,on/off)
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
        print('state changed {}:{}'.format(self.state,next_state))            
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
                if len(item[2])>1:
                    for func in item[2]:
                        print(func)
                        self.output.append(func)
                else:
                    print(item[2])
                    self.output.append(item[2])
                self.clock_list.remove(item)  

    def activate(self,on):
        if on:
            self.active = 1
            self.state = 0
            print('{} activated'.format(self.name))
        else:
            self.active = 0
            print('{} deactivated'.format(self.name))
     


    
