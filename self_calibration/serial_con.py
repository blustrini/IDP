'''
Establishes serial connection to the arduino
'''

import serial
from subprocess import *

#change this
try:
    board = serial.Serial("/dev/tty.usbmodem144101", 9600)
# This creates an object able to establish a serial communication channel
# with the board. The first parameter depends on your operating system
# and probably needs to be updated.
# The second is the baud rate. It needs to match the board's settings.

except:
    print('Serial connection not established')

def read_serial():
    #read serial output from board
    try:
        return board.readline()
    except NameError:
        print('Error: the board had not been defined')

def write_serial(msg):
    board.write(msg)

