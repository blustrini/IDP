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
    	Calibrate.triggers[serial_in]()
    #catch error if no line has been read
    except KeyError:
    	pass

    for i in Calibrate.output:
        write_serial(i)
