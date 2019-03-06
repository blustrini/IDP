from task import *
import time

class Block_Sort(Task):
    def __init__(self,Dim):
        #initialise superobject
        super().__init__(Dim)
        #name
        self.name = 'Block_Sort'

        #flowchart        0         1          
        #               idle,   rotate_wheel

        #dictionaries represent reaction to trigger based on current state
        self.block_at_wheel = {
        0 : (('w_r'),1),          #move forward, goto state 1
        1 : ((),1)           #move backward goto state 
        }


        #processing actions
        self.processes = {
        '01' : (self.wheel_360)
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '7' : self.block_at_wheel
        }

    def wheel_360:
        time1 = time.time()
        wait1 = 3 #calibrate this with the wheel
        func1 = self.action_dict['w_s']
        tuple1 = (time1,wait1,func1)
        self.clock_list.append(tuple1)
        self.change_state(0)





