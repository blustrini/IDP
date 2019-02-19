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
    Calibrate.triggers[serial_in]()

    for i in Calibrate.output:
        write_serial(i)


    

