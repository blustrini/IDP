'''
Not used in final code
'''


from serial_con import *

port = find_usb_port()

board = serial.Serial(port,9600)

board.close()