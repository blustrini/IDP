'''
The main loop of the program
'''
#import modules
from serial_con import *
from process import *

#initialise progress object
Process = Process()


#main loop
while True:
    serial_in = read_serial()
    Process.triggers[serial_in]()

    for i in Process.output:
        write_serial(i)


    

