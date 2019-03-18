import serial
import matplotlib.pyplot as plt
import time
import glob

'''
Wasn't used in final version
'''

def find_usb_port():
    #gets list of ports
    ports = glob.glob('/dev/tty.*')

    #finds usb port
    for port_test in ports:
    	if 'usb' in port_test:
    		return port_test
    print('no port found')
    return 0

def establish_serial(port,board):
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

board = serial.Serial(find_usb_port(),9600)

while True:
    board.write(b'led_on')
    time.sleep(2)
        



    #print(line) prints just the binary

