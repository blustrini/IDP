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

        #subprocesses
        self.Switch_front = Subprocess()
        self.Switch_back = Subprocess()

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        b'switch_front': self.Switch_front,
        b'switch_back': self.Switch_back}

        #output
        self.output = []





    
