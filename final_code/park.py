import time
from task import *

'''
Task parks teh robot after blocks have been dropeed
'''

class Park(Task):
    def __init__(self,Dim):
        #initialise super object
        super().__init__(Dim)
        #name
        self.name = 'Park'


        #flowchart        0         1         2
        #               idle,   align wall, reverse, 

        self.switch_front = {
        0 : ((),0), #ignore
        1 : (('b'),2), #goto state 2
        2 : ((),2)
        }

        self.switch_back = {
        0 : ((),1), #goto state 1
        1 : ((),1), #ignore
        2 : (('f'),2) #add a third state for failsafe?
        }

        self.processes = {
        '01' : (self.init_htl),
        '12' : (self.time_park),

        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back}

    #turning functions
    def init_htl(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht
        func1 = self.half_turn_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1

    def half_turn_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_ht
        func1 = self.action_dict['f']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['l'])
        self.clock_list.append(tuple1)
        return 1

    def time_park(self):
        time1 = time.time()
        wait = self.Dim.wait_park
        func1 = self.action_dict['s']
        tuple1 = (time1,wait,func1)
        self.clock_list.append(tuple1)







