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

        #processing actions
        self.processes = {
        '12' : (self.start_timer),
        '23' : (self.end_timer,self.start_timer),
        '34' : (self.end_timer,self.calibrate),#calc calibration
        '40' : (self.print_calibration_data)
        }

        #processing functions -----------------------

        #initialise time saving attributes
        self.time = 0
        self.time_list = []
        #initialise calibration value
        self.calibrated_value = 1



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
        #create the key for the processes dictionary
        key = str(self.state)+str(next_state)
        #call the relevant processes
        for i in self.processes[key]:
            i.()
        #update state
        self.state = next_state

        return 1

    def start_timer(self):
        self.time = time.time()
        return 1

    def end_timer(self):
        end_time = time.time()
        self.time_list.append(end_time-self.time)
        self.time = 0
        return 1

    def print_calibration_data(self):
        print(self.calibration_value)
        return 1


    
