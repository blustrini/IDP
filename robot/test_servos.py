from task import *

class Test_Servos(Task):
    def __init__(self,Dim):
        #initialise superobject
        super().__init__(Dim)
        #name
        self.name = 'Test Servos'
        self.state = 0
        
        #flowchart        0             1           2           3           4           5
        #               exit zone, turn left, goto centre, turn right, drop blocks, align return

        #dictionaries represent reaction to trigger based on current state
        self.switch_front = {
        0 : (('A'),0),          #move back, goto state 1
           #ignore
        }
        
        self.switch_back = {
        0 : (('E'),0),          #failsafe
        }
        
        
        #processing actions
        self.processes = {
        '00' : self.sanity,
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back
        }

    def sanity(self):
        print('yup')










