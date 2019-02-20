'''
Establishes serial connection to the arduino
'''
import glob
import serial

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

def read_next_line(board):
    #read serial output from board
    try:
        line = board.readline()
        return(line)
    except:
        print('Failed')
       # print('Error: Couldn\'t read line from serial')

def read_latest_line(board):
    latest = board.readline()
    discarded = [latest]
    i = 0
    while board.inWaiting() > 0 and i < 100000:
        i+= 1
        latest = board.readline()
        discarded.append(latest)
    return (latest,discarded)

def write_serial(msg):
    try:
        board.write(msg)
    except:
        print('Error: Couldn\'t write line to serial')
