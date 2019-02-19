'''
Establishes serial connection to the arduino
'''
import glob
import serial
from subprocess import *

def find_usb_port():
    #gets list of ports
    ports = glob.glob('/dev/tty.*')

    #finds usb port
    for port_test in ports:
    	if 'usb' in port_test:
    		return port_test
    
    return 0

def establish_serial(port):
    #create serial connection to board
    try:
    	board = serial.Serial(port,9600)
    #raise error if no usb port is found
    except ValueError:
        print('ValueError: No USB port found')
        return 0
    except OSError:
        print('OSError: Couldn\'t connect to port')
        return 0
    return 1

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

establish_serial(find_usb_port())
print(find_usb_port())
