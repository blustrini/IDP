from task import *

class Block_Detect(Task):
    def __init__(self,Dim):
        #initialise superobject
        super().__init__(Dim)
        #name
        self.name = 'Block_Detect'

        #flowchart        0         1           2       3
        #               idle, measure magnet, accept, reject

        #dictionaries represent reaction to trigger based on current state
        self.block_detect = {
        0 : (('s'),1),          #move forward, goto state 1
        1 : ((),1),             #move backward goto state 2
        2 : ((),2),
        3 : ((),3)
        }
        
        self.hall_detect = {
        0 : ((),2),          #move forward, goto state 1
        1 : ((),2),             #ignore, stay in state 1
        2: ((),2),
        3: ((),3)
        }

        #processing actions
        self.processes = {
        '01' : (self.timoeut_hall),
        '12' : (self.accept),
        '13' : (self.reject),
        '20' : (self.goforward),
        '30' : (self.goforward),
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '5' : self.block_detect,
        '6' : self.hall_detect}

    def timeout_hall(self):
        time1 = time.time()
        wait = 3  #change this accordingly
        func1 = self.check_reject
        tuple1 = (time1,wait,func1)
        self.clock_list.append(tuple1)

    def check_reject(self):
        if self.state == 2:
            pass
        elif self.state == 1:
            self.change_state(3)

    def reject(self):
        self.output.append(self.action_dict['s_rej'])
        self.change_state(0)

    def accept(self):
        self.output.append(self.action_dict['s_acc'])
        self.change_state(0)

    def goforward(self):
        self.Dim.pid = True
        if self.Dim.pid_side == 'l':
            self.output.append(self.action_dict['p_l'])
        else:
            self.output.append(self.action_dict['p_r'])
        self.output.append(self.action_dict['f'])









