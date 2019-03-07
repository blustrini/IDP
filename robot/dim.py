#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 10:03:14 2019

@author: ongrayyi
"""

class Dim():
    def __init__(self):
        self.arena_length = 240
        self.arena_width = 240
        self.robot_length = 39.2
        self.robot_width = 20
        self.speed = 10
        self.pid = False
        self.pid_side = 'l'
        self.wait_hall = 3
        self.wait_block = 3
        self.wait_wheel = 3
        self.wait_drop = 5
        self.wait_init_ht = 1.2
        self.wait_init_st = 2
        self.wait_init_ft
        self.wait_ht = 2
        self.wait_ft = 0.6
        self.wait_pivot = 2.3
        self.wait_st = 3.2
        self.wait_align = 1
        self.wait_park = 1