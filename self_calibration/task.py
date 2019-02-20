'''
The task the is currently being performed. This will be the most high-level class, so the task must be high-level

N.B. This Task is defined specifically to perform a Calibration task.

Task object should be rewritten generally and class inheritance can be used to perform different tasks.
'''
from actions import *

class Task():
    def __init__(self):
        '''
        flowchart
                  0         1          2           3            4
        states: idle, align_back, goto_front, goto_back, calibration_test
        '''
        #current state
        self.state = 0

        action_dict = {
        'f' : b'move_forwards',
        'b' : b'move_back',
        's' : b'move_stop'
        }

        #modifiable function holding possible actions associated with the task
        self.Actions = Actions(self,action_dict)

        stages = [0]

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
        3 : (('s','f'),4),      #stop, move forward, goto state 4
        4 : ((),4) }            #ignore, stay in state 4

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        b'switch_front': self.switch_front,
        b'switch_back': self.switch_back}

        #output
        self.output = []


'''
The end goal is to be able to call the following from the main loop:
- Task.triggers[read_serial][Task.state]()

i.e. identify what the arduino has said, and interpret the trigger in the context of the current task being performed

Currently, the output is saved in an attribute of the main Task class
'''






    
