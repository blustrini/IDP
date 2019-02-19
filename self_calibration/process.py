'''
The brains of the process, through oop
'''
#import subprocess class
from subprocess import *

class Process():
    def __init__(self):
        #flowchart
        #          0         1          2           3            4
        #stages: idle, align_back, goto_front, goto_back, calibration_test
        #current state
        self.state = 0
        self.Actions = Robot_Actions()

        stages = [0]

        #subprocesses
        self.switch_front = #dictionary
        self.switch_back = #dictionary

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        b'switch_front': self.switch_front,
        b'switch_back': self.switch_back}

        #output
        self.output = []




-----------------------

        Process.triggers[read_serial][Process.state]()







    
