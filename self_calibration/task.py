'''
The task the is currently being performed. This will be the most high-level class, so the task must be high-level

N.B. This Task is defined specifically to perform a Calibration task.

Task object should be rewritten generally and class inheritance can be used to perform different tasks.
'''
import time

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
        3 : (('s','f'),4),      #stop, move forward, goto state 4
        4 : ((),4) }            #ignore, stay in state 4

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        b'sf': self.switch_front,
        b'sb': self.switch_back}

        #all processes to be carried out on state switches
        self.processes = {
        #maps state switch to process
        }

        #output
        self.output = []

    #get list of instructions, in the given order
    def get_instructions(self,data):
        #initialise list
        list = []
        #get instructions corresponding to each item in list
        for i in data[0]:
            list.append(self.action_dict[i])
        #change state
        self.change_state(data[1])
        #return list of instructions ready for writing on serial
        return list

    #change state and perform any functions associated with change of state
    def change_state(self,next_state):
        '''
        need to add a dictionary that maps state switch to required processing functions
        '''
        #update state
        self.state = next_state



    
