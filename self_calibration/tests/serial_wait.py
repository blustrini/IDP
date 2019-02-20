
import glob
import serial
import time

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
    return board

def read_serial(board):
    #read serial output from board
    try:
        line = board.readline()
        print(line.decode())
        return(line)
    except:
        print('Failed')
       # print('Error: Couldn\'t read line from serial')

def write_serial(msg):
    try:
        board.write(msg)
    except:
        print('Error: Couldn\'t write line to serial')

board = establish_serial(find_usb_port())


def getLatestStatus(board):
    status = board.readline()
    while board.inWaiting() > 0:
        status = board.readline()
    return status

while True:
    line = board.readline()
    print(line)
    line2 = getLatestStatus(board)
    print(line2)

