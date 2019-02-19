'''
Establishes serial connection to the arduino
'''
import glob
import serial
from subprocess import *

#gets list of ports
ports = glob.glob('/dev/tty.*')

#finds usb port
for port_test in ports:
	if 'usbmodem' in port_test:
		port = port_test
		break

#create serial connection to board
try:
	board = serial.Serial(port,9600)
#raise error if no usb port is found
except NameError:
	raise NameError('No USB port found')
except OSError:
	raise OSError('Couldn\'t connect to port')

def read_serial():
    #read serial output from board
    try:
        return board.readline()
    except:
        print('Error: Couldn\'t read line from serial')

def write_serial(msg):
    try:
        board.write(msg)
    except:
        print('Error: Couldn\'t write line to serial')