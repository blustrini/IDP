'''
The main loop of the program
'''
#import modules
from serial_con import *
from task import *

#initialise progress object
Calibrate = Task()


#main loop
while True:
    serial_in = read_serial()

    #feed line into task object
    try:
    	instructions = Calibrate.Actions(Calibrate.triggers[serial_in][Calibrate.state])
    #catch error if no line has been read
    except KeyError:
    	instructions = []

    #write all instructions to serial
    for i in instructions:
        write_serial(i)

'''
Think about timing here, especailly in the write_serial loop. Perhaps some handshaking is required, etc...
Furthermore, serial_in could be modified to return a list of the most important triggers from the serial since the last reset of the loop
--> this would make the whol ething work regardless of the loop time
'''