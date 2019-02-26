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
        
        #dictionaries represent reaction to trigger based on current state
        self.switch_front = {
        0 : (('f'),1),          #move forward, goto state 1
        1 : ((),2),             #move backward, wait, 90 degree left turn, move backward, goto state 5
        2 : ((),3),             #move backward, wait, 180 degree left turn, move backward, goto state 3
        3 : ((),3),             #ignore, stay in state 3
        4 : ((),5),             #move backward, wait, 180 degree right turn, move backward, goto state 5
        5 : ((),5),             #ignore, stay in state 5
        }
        
        self.switch_back = {
        0 : (('f'),1),          #move forward, goto state 1
        1 : ((),1),             #ignore, stay in state 1
        2 : ((),2),             #ignore, stay in state 2
        3 : (('f'),4),          #move forward, goto state 4
        4 : ((),4),             #ignore, stay in state 4
        5 : (('f'),5),          #move forward, goto state 2
        }
        
        #processing actions
        self.processes = {
        '12' : (self.half_turn_left),
        '23' : (self.full_turn_left),
        '45' : (self.half_turn_right),
        }
        
    def half_turn_left(self):
        #start,wait,func
        self.output.append(self.action_dict['b'])
        time1 = time.time()
        wait1 = 10/self.Dim.speed
        func1 = self.action_dict['l']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        wait2 = wait1 + 3 #calculate with actual dimensions
        func2 = self.action_dict['b']
        tuple2 = (time1,wait2,func2)
        self.clock_list.append(tuple1)
        self.clock_list.append(tuple2)
        return 1
        
    def full_turn_left(self):
        #start,wait,func
        self.output.append(self.action_dict['b'])
        time1 = time.time()
        wait1 = 10/self.Dim.speed
        func1 = self.action_dict['L']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        wait2 = wait1 + 5
        func2 = self.action_dict['b']
        tuple2 = (time1,wait2,func2)
        self.clock_list.append(tuple1)
        self.clock_list.append(tuple2)
        return 1
    
    def full_turn_right(self):
        #start,wait,func
        self.output.append(self.action_dict['b'])
        time1 = time.time()
        wait1 = 10/self.Dim.speed
        func1 = self.action_dict['R']
        tuple1 = (time1,wait1,func1)
        print(tuple1)
        wait2 = wait1 + 5
        func2 = self.action_dict['b']
        tuple2 = (time1,wait2,func2)
        self.clock_list.append(tuple1)
        self.clock_list.append(tuple2)
        return 1
    