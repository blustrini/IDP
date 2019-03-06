from task import *

class Block_Sort(Task):
        def __init__(self,Dim):
                #initialise superobject
                super().__init__(Dim)
                #name
                self.name = 'Block_Sort'

        #flowchart        0         1        2   
        #               idle,   accept,    reject

        #dictionaries represent reaction to trigger based on current state
        self.block_detect = {
        0 : ((),),          #move forward, goto state 1
        1 : ((),),             #move backward goto state 2
        2 : ((),),             #unexpected trigger, maybe do some error fixing later
        3 : ((),),             #move back, goto state 4
        4 : ((),),             #unexpected trigger, maybe do some error fixing later
        5 : ((),)            #ignore, stay in state 5
        }
        
        self.hall_detect = {
        0 : ((),),          #move forward, goto state 1
        1 : ((),),             #ignore, stay in state 1
        2 : ((),),             #add clock that aliogns robot with wall, goto state 3
        3 : ((),),          #unexpected trigger, maybe do some error fixing later n.b. back switch might be triggered by align mechanism
        4 : ((),),             #add clock that aliogns robot with wall, goto state 3
        5 : ((),)         #move forward, goto state 2
        }

        #processing actions
        self.processes = {
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '5' : self.block_detect,
        '6' : self.hall_detect}