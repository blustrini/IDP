#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:50:33 2019

@author: ongrayyi
"""
import time
from task import *

'''
Task handles entering the field and sweeping
'''

class Navigate(Task):
    def __init__(self,Dim):
        #initialise super object
        super().__init__(Dim)
        #name
        self.name = 'Navigate'

        #attributes
        self.sweeps = 1
        
        #flowchart        0         1             2             3               4              5				6
        #               idle, enter field, align first sweep, do 1 sweep, align next sweep, initiate leave, go back

        #dictionaries represent reaction to trigger based on current state
        self.switch_front = {
        0 : (('b',),0),          #move forward, goto state 1
        #0 : (('F',),0),          #move forward, goto state 1
        1 : (('b'),2),             #move backward goto state 2
        2 : ((),2),             #unexpected trigger, maybe do some error fixing later
        #3 : (('p_s','s_block','b'),4),             #move back, goto state 4 #change!!!!
        3 : (('b'),4),             #move back, goto state 4 #change!!!!
        4 : ((),4),             #unexpected trigger, maybe do some error fixing later
        5 : ((),0)             #ignore
        }
        
        self.switch_back = {
        0 : (('f'),1),          #move forward, goto state 3
        1 : ((),1),             #ignore, stay in state 1
        2 : (('b'),3),             #add clock that aliogns robot with wall, goto state 3
        3 : ((),3),          #ignore
        4 : (('b'),3),             #add clock that aliogns robot with wall, goto state 3
        5 : (('f'),0),          #stop and goto state 0
        6 : (('b'),2)
        }
        
        #processing actions
        self.processes = {
        '00' : (self.align_back_wall_zero),
        '01' : (self.align_back_wall),
        '12' : (self.init_htl_first,self.stop_block_detect),
        '23' : (self.align_back_wall_first,self.start_block_detect),
        '43' : (self.align_back_wall,self.start_block_detect),
        #'34' : (self.stop_pid,self.stop_block_detect,self.check_sweeps),
        '34' : (self.stop_block_detect,self.check_sweeps),
        '45' : (self.init_htl_final,self.init_drop_payload),
        '50' : (),
        '30' : (),
        '61' : (self.align_back_wall)

        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back}


    def init_drop_payload(self):
    	#initialise drop_payload task
        func1 = self.drop_payload
        time1 = time.time()
        #wait1 = 2
        wait1 = 5
        tuple1 = (time1,wait1,func1)
        self.clock_list.append(tuple1)
    
    def drop_payload(self):
        self.task_control.append(('Drop_Payload',1,1))

    def stop_block_detect(self):
    	#block detection is stopped during turning to allow for pile-ups to flush out through rejection chute
        self.task_control.append(('Block_Detect',0,1))

    def start_block_detect(self):
    	#reinstate block_detect
        self.task_control.append(('Block_Detect',1,1))
        #self.output.append(self.action_dict['A'])
       
       
    def align_back_wall(self):
    	#ram into back wall to make robot straight
        print('align back wall')
        time1 = time.time()
        wait1 = self.Dim.wait_align
        func1 = self.action_dict['f']
        #func1 = self.start_pid()
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        
    def align_back_wall_zero(self):
        print('align back wall')
        time1 = time.time()
        wait1 = self.Dim.wait_align + 2
        func1 = self.action_dict['f']
        #func1 = self.start_pid()
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        
    def align_back_wall_first(self):
        print('align back wall')
        time1 = time.time()
        wait1 = self.Dim.wait_align
        func1 = self.init_correct
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)

       '''
       deprecated pid code
        
    def start_pid(self):
        if self.sweeps % 2 == 1:
            self.output.append(self.action_dict['p_r'])
            self.Dim.pid_side = 'r'
        else:
            self.output.append(self.action_dict['p_l'])
            self.Dim.pid_side = 'l'
        self.output.append(self.action_dict['f'])
        self.Dim.pid = True

    def stop_pid(self):
        self.Dim.pid = False

		'''
    def check_sweeps(self):
    	#check how many sweeps have been done todetermine turning direction
        print('sweeps = {}'.format(self.sweeps))
        if self.sweeps >= 5:
            '''
            time1 = time.time()
            wait1 = 1.5
            func1 = self.to_state_5
            tuple1 = (time1,wait1,func1)
            self.clock_list.append(tuple1)
            '''
            self.change_state(5)
        elif self.sweeps % 2 == 1:
            self.init_ftl()
            self.sweeps += 1
        else:
            self.init_ftr()
            self.sweeps += 1
        

    #turning functions
    def init_htl_final(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht
        func1 = self.half_turn_left_final
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1
    
    #turning functions
    def init_htl(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht
        func1 = self.half_turn_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1

     #turning functions
    def init_htl_first(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ht + 1
        func1 = self.half_turn_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1

    def half_turn_left_final(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_ht
        #func1 = self.action_dict['f']
        func1 = self.after_half_turn_left_final
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['l'])
        self.clock_list.append(tuple1)
        return 1
    
    def after_half_turn_left_final(self):
        self.output.append(self.action_dict['f'])
    
    def half_turn_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_ht
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['l'])
        self.clock_list.append(tuple1)
        return 1

    def init_correct(self):
    	#correct for the first turn when entering the field
        time1 = time.time()
        wait1 = self.Dim.wait_init_correct
        func1 = self.correct_right
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['f'])
        self.clock_list.append(tuple1)
        return 1

    
    def correct_right(self):
        time1 = time.time()
        wait1 = self.Dim.wait_correct_r
        func1 = self.slight_forward
        #func1 = self.action_dict['f']
        #func1 = self.correct_left
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['R'])
        self.clock_list.append(tuple1)
        return 1

    def slight_forward(self):
        time1 = time.time()
        wait1 = self.Dim.wait_forward
        func1 = self.correct_left
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['f'])
        self.clock_list.append(tuple1)
        return 1  

        
    def correct_left(self):
        time1 = time.time()
        wait1 = self.Dim.wait_correct_l
        #func1 = self.action_dict['F']
        func1 = self.action_dict['f']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['L'])
        self.clock_list.append(tuple1)
        return 1
        #MORE TO DO

    def init_ftl(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ft
        func1 = self.pivot_ninety_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1
        
    def pivot_ninety_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_pivot
        func1 = self.forwards_before_reverse_l
        #func1 = self.reverse_before_soft_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['L'])        
        self.clock_list.append(tuple1)
        return 1
    
    def forwards_before_reverse_l(self):
        time1 = time.time()
        wait1 = self.Dim.wait_forward_reject
        func1 = self.reverse_before_soft_left
        tuple1 = (time1,wait1,func1)
        self.clock_list.append(tuple1)
        self.output.append(self.action_dict['f'])
    
    def reverse_before_soft_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_st + self.Dim.wait_forward_reject #remove second wait if not going forward
        func1 = self.soft_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['b'])        
        self.clock_list.append(tuple1)
        return 1
    
    def soft_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_st
        #func1 = self.action_dict['b']
        func1 = self.reverse_after_soft_turn
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['l'])        
        self.clock_list.append(tuple1)
        return 1

    def init_ftr(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_ft
        func1 = self.pivot_ninety_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1
        
    def pivot_ninety_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_pivot
        #func1 = self.forwards_before_reverse_r
        func1 = self.reverse_before_soft_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['R'])        
        self.clock_list.append(tuple1)
        return 1
    
    def forwards_before_reverse_r(self):
        time1 = time.time()
        wait1 = self.Dim.wait_forward_reject
        func1 = self.reverse_before_soft_right
        tuple1 = (time1,wait1,func1)
        self.clock_list.append(tuple1)
        self.output.append(self.action_dict['f'])
    
    def reverse_before_soft_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_st #+ self.Dim.wait_forward_reject #remove if not going forwards
        func1 = self.soft_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['b'])        
        self.clock_list.append(tuple1)
        return 1
    
    def soft_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_st
        func1 = self.reverse_after_soft_turn
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['r'])        
        self.clock_list.append(tuple1)
        return 1
    
    #ADDED
    def reverse_after_soft_turn(self):
        time1 = time.time()
        wait1 = self.Dim.timeout
        func1 = self.to_state_3
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        self.output.append(self.action_dict['b'])

    #some functions to call state changes after delays
    def to_state_3(self):
        self.change_state(3)
    
    def to_state_5(self):
        self.change_state(5)
    