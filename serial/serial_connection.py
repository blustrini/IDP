import serial
from subprocess import *
import matplotlib.pyplot as plt
import time

board = serial.Serial("/dev/tty.usbmodem144101", 9600)
# This creates an object able to establish a serial communication channel
# with the board. The first parameter depends on your operating system
# and probably needs to be updated.
# The second is the baud rate. It needs to match the board's settings.


while True:
    board.write(b'led_on')
    time.sleep(2)
        



    #print(line) prints just the binary

