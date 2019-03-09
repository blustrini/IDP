#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 10:03:14 2019

@author: ongrayyi
"""

class Dim():
    def __init__(self):
        #dimensions
        self.arena_length = 240
        self.arena_width = 240
        self.robot_length = 39.2
        self.robot_width = 20
        #calibrated
        self.speed = 11
        #pid
        self.pid = False
        self.pid_side = 'r'
        #bloc detection waits
        self.wait_hall = 3
        self.wait_block = 3
        self.wait_wheel = 3
        self.wait_drop = 5
        #turning waits
        self.wait_init_ht = 1.5
        self.wait_init_st = 1.3
        self.wait_init_ft = 1.2
        self.wait_ht = 3.7
        self.wait_ft = 1
        self.wait_pivot = 2.4
        self.wait_st = 3.3
        self.wait_align = 1
        self.wait_init_correct = 0.2
        self.wait_correct_r = 0.2
        self.wait_correct_l = 0.2
        self.wait_forward = 3.7

        #parking wait
        self.wait_park = 0.5