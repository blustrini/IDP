from task import *

'''
This task handles driving to the depositing station and depositing blocks
'''

class Drop_Payload(Task):
    def __init__(self,Dim):
        #initialise superobject
        super().__init__(Dim)
        #name
        self.name = 'Drop_Payload'
        
        #flowchart        0             1           2           3           4           5
        #               exit zone, turn left, goto centre, turn right, drop blocks, align return

        #dictionaries represent reaction to trigger based on current state
        self.switch_front = {
        0 : (('b'),1),          #move back, goto state 1
        1 : ((),1),             #ignore
        2 : ((),2),             #trigger emergency calibrate?
        3 : (('s','O'),4),    #stop, goto state 4
        4 : ((),4),             #ignore
        5 : ((),5)             #ignore
        }
        
        self.switch_back = {
        0 : (('f'),0),          #failsafe
        1 : (('b'),2),          #ram into wall, goto state 2
        2 : (('f'),2),          #failsafe
        3 : ((),3),             #ignore
        4 : ((),4),             #ignore
        5 : ((),0)          #ignore
        }
        
        #processing actions
        self.processes = {
        '01' : (self.init_htl,self.turnoff_nav),
        '12' : (self.align_back_wall),
        '23' : (self.init_htr),
        '34' : (self.wait_for_blocks),
        '45' : (self.init_htr_back),
        '50': (self.turnoff)
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back
        }

    def turnoff_nav(self):
    	#turn off navigation task once danger zone has been left
        self.task_control.append(('Navigate',0,0))

    def turnoff(self):
    	#turnoff self once parking has initiated
        self.active = 0

    def wait_for_blocks(self):
    	#delay to allow time for blocs to fall onto collection platform
        time1 = time.time()
        wait1 = self.Dim.wait_drop
        func1 = self.init_statechange_45
        tuple1 = (time1,wait1,func1)
        self.clock_list.append(tuple1)

    def init_statechange_45(self):
        self.output.append(self.action_dict['b'])
        self.change_state(5)


    #turning functions
    def init_htr_back(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht + 2
        func1 = self.half_turn_right_back
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1

    def init_htr(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht
        func1 = self.half_turn_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['b'])
        self.clock_list.append(tuple1)
        return 1

    def half_turn_right_back(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_ht
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['r'])
        self.clock_list.append(tuple1)
        self.task_control.append(('Park',1,1))
        return 1

    def half_turn_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_ht
        func1 = self.action_dict['f']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['r'])
        self.clock_list.append(tuple1)
        return 1


    def init_htl(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht + 4
        func1 = self.half_turn_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1

    def half_turn_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_ht
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['l'])
        self.clock_list.append(tuple1)
        return 1

    def align_back_wall(self):
        print('align back wall')
        time1 = time.time()
        wait1 = self.Dim.wait_align
        func1 = self.drive_to_centre
        #func1 = self.start_pid()
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)


    def drive_to_centre(self):
    	#drives to the centre of the arena based of off previously calibrated speed variable
        time1 = time.time()
        wait1 = (0.5*self.Dim.arena_width-self.Dim.robot_length)/self.Dim.speed
        func1 = self.init_statechange_23
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['f'])
        self.clock_list.append(tuple1)

    def init_statechange_23(self):
        self.output.append(self.action_dict['s'])
        self.change_state(3)











