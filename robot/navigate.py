#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 12:50:33 2019

@author: ongrayyi
"""
import time
from task import *

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
        0 : (('f',),1),          #move forward, goto state 1
        1 : (('b'),2),             #move backward goto state 2
        2 : ((),2),             #unexpected trigger, maybe do some error fixing later
        #3 : (('p_s','s_block','b'),4),             #move back, goto state 4 #change!!!!
        3 : (('s_block','b'),4),             #move back, goto state 4 #change!!!!
        4 : ((),4),             #unexpected trigger, maybe do some error fixing later
        5 : ((),0)             #ignore
        }
        
        self.switch_back = {
        0 : (('b'),6),          #move forward, goto state 3
        1 : ((),1),             #ignore, stay in state 1
        2 : (('b'),3),             #add clock that aliogns robot with wall, goto state 3
        3 : ((),3),          #ignore
        4 : (('b'),3),             #add clock that aliogns robot with wall, goto state 3
        5 : (('f'),0),          #stop and goto state 0
        6 : (('b'),1)
        }
        
        #processing actions
        self.processes = {
        '12' : (self.init_htl),
        '23' : (self.align_back_wall_first,self.start_block_detect),
        '43' : (self.align_back_wall,self.start_block_detect),
        #'34' : (self.stop_pid,self.stop_block_detect,self.check_sweeps),
        '34' : (self.stop_block_detect,self.check_sweeps),
        '45' : (self.init_htl),
        '50' : (self.init_drop_payload),
        '30' : (self.stop_and_flush),
        '61' : (self.align_back_wall)

        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back}

    def stop_and_flush(self):
        self.state = 0
        self.clock_list = []


    def init_drop_payload(self):
        self.task_control.append(('Drop_Payload',1,1))
        time1 = time.time()
        wait1 = 2
        func1 = self.stop_and_flush
        tuple1 = (time1,wait1,func1)
        self.clock_list.append(tuple1)

    def stop_block_detect(self):
        self.task_control.append(('Block_Detect',0,1))

    def start_block_detect(self):
        self.task_control.append(('Block_Detect',1,1))
        self.output.append(self.action_dict['s_acc'])
       
       #ram into back wall to mae robot straight
    def align_back_wall(self):
        print('align back wall')
        time1 = time.time()
        wait1 = self.Dim.wait_align
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

    def check_sweeps(self):
        if self.sweeps >= 5:
            self.change_state(5)
        elif self.sweeps % 2 == 1:
            self.init_ftl()
        else:
            self.init_ftr()
        self.sweeps += 1


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
        func1 = self.reverse_before_soft_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['L'])        
        self.clock_list.append(tuple1)
        return 1
    
    def reverse_before_soft_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_st
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
        func1 = self.action_dict['b']
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
        func1 = self.reverse_before_soft_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['R'])        
        self.clock_list.append(tuple1)
        return 1
    
    def reverse_before_soft_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = self.Dim.wait_init_st
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
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['r'])        
        self.clock_list.append(tuple1)
        return 1
    