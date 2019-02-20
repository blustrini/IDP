'''
The main loop of the program
'''
#import modules
from serial_con import *
from task import *


#create board object
board = establish_serial(find_usb_port())

print('board')

#initialise progress object
#Calibrate = Task()

n = 10

i = -1
#main loop
while True:
	i += 1
	i = i%10

	if i != 0:
	    serial_in = read_next_line(board)
	    print('line: {}'.format(serial_in))

	else:
		serial_in = read_latest_line(board)
		print(serial_in[1])

	

'''
#feed line into task object
try:
	instructions = Calibrate.Actions.get_instructions(Calibrate.triggers[serial_in][Calibrate.state])
#catch error if no line has been read
except KeyError:
	instructions = []

#write all instructions to serial
for i in instructions:
    write_serial(i)
'''
'''
Think about timing here, especailly in the write_serial loop. Perhaps some handshaking is required, etc...
Furthermore, serial_in could be modified to return a list of the most important triggers from the serial since the last reset of the loop
--> this would make the whol ething work regardless of the loop time
'''