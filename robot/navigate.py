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
        
        #flowchart        0         1             2             3               4           5
        #               idle, enter field, align first sweep, do 1 sweep, align next sweep, initiate leave

        #dictionaries represent reaction to trigger based on current state
        self.switch_front = {
        0 : (('d'),1),          #move forward, goto state 1
        1 : (('b'),2),             #move backward goto state 2
        2 : ((),2),             #unexpected trigger, maybe do some error fixing later
        3 : (('b'),4),             #move back, goto state 4
        4 : ((),4),             #unexpected trigger, maybe do some error fixing later
        5 : (('s'),0),             #ignore, stay in state 5
        }
        
        self.switch_back = {
        0 : (('d'),1),          #move forward, goto state 1
        1 : ((),1),             #ignore, stay in state 1
        2 : (('b'),3),             #add clock that aliogns robot with wall, goto state 3
        3 : ((),3),          #unexpected trigger, maybe do some error fixing later n.b. back switch might be triggered by align mechanism
        4 : (('b'),3),             #add clock that aliogns robot with wall, goto state 3
        5 : (('s'),0),          #move forward, goto state 2
        }
        
        #processing actions
        self.processes = {
        '12' : (self.init_htl),
        '23' : (self.align_back_wall_first),
        '43' : (self.align_back_wall),
        '34' : (self.check_sweeps),
        '45' : (self.init_htl)
        }

        #all possible actions mapped to the corresponding arduino outputs
        self.triggers = {
        '3' : self.switch_front,
        '4' : self.switch_back}
       
       #ram into back wall to mae robot straight
    def align_back_wall(self):
        print('align back wall')
        time1 = time.time()
        wait1 = 1
        func1 = self.action_dict['f']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        
    def align_back_wall_first(self):
        print('align back wall')
        time1 = time.time()
        wait1 = 1
        func1 = self.action_dict['d']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)

    def check_sweeps(self):
        if self.sweeps >= 3:
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
        wait1 = 2/self.Dim.speed
        func1 = self.half_turn_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1

    def half_turn_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 1.2 #calculate with actual dimensions
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        self.output.append(self.action_dict['l'])
        self.clock_list.append(tuple1)
        return 1

    def init_ftl(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 10/self.Dim.speed
        func1 = self.pivot_ninety_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1
        
    def pivot_ninety_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 2.3 #add real value
        func1 = self.reverse_before_soft_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['L'])        
        self.clock_list.append(tuple1)
        return 1
    
    def reverse_before_soft_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 2 #add real value
        func1 = self.soft_left
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['b'])        
        self.clock_list.append(tuple1)
        return 1
    
    def soft_left(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 2.5 #add real value
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['l'])        
        self.clock_list.append(tuple1)
        return 1

    def init_ftr(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 10/self.Dim.speed
        func1 = self.full_turn_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.clock_list.append(tuple1)
        return 1
        
    def pivot_ninety_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 2.3 #add real value
        func1 = self.reverse_before_soft_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['R'])        
        self.clock_list.append(tuple1)
        return 1
    
    def reverse_before_soft_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 2 #add real value
        func1 = self.soft_right
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['b'])        
        self.clock_list.append(tuple1)
        return 1
    
    def soft_right(self):
        #start,wait,func
        time1 = time.time()
        wait1 = 2.5 #add real value
        func1 = self.action_dict['b']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        self.output.append(self.action_dict['r'])        
        self.clock_list.append(tuple1)
        return 1
    