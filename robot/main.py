'''
The main loop of the program
'''
#import modules
from serial_con import *
from task import *
from dim import *
from calibrate_dist import *
from navigate import *
from block_pickup import *
from block_detect2 import *
from drop_payload import *
from park import *

#create board object
board = establish_serial(find_usb_port())

print('board')

#initialise dimension object
Dim = Dim()

#initialise tasks
Park = Park(Dim)
Drop_Payload = Drop_Payload(Dim)
Block_Pickup = Block_Pickup(Dim)
Block_Detect = Block_Detect(Dim)
Calibrate_Dist = Calibrate_Dist(Dim)
Navigate = Navigate(Dim)


#create list of tasks
tasks = [Calibrate_Dist,Navigate,Block_Detect,Block_Pickup,Drop_Payload,Park]
#create dict of tasks
tasks_dict = {
    'Park':Park,
    'Calibrate_Dist':Calibrate_Dist,
    'Navigate':Navigate,
    'Block_Pickup':Block_Pickup,
    'Block_Detect':Block_Detect,
    'Drop_Payload':Drop_Payload
}
Park.active = 0
Calibrate_Dist.active = 0
Navigate.active = 0
Block_Pickup.active = 0
Block_Detect.active = 0
Drop_Payload.active = 1

Navigate.state = 1


#main loop
while True:
    #get serial input
    serial_in = read_next_line(board,decode=True,strip=True)
    if serial_in == 6:
        if Dim.block_detected:
            while serial_in == '6':
                serial_in = read_next_line(board,decode=True,strip=True)
            Dim.block_detected = False
        else:
            Dim.block_detected = True

    #print serial input
    if serial_in != None:
        print(serial_in)

    #pass input into all tasks
    for Task in tasks:
        if Task.active == 1:
            #feed line into task object
            try:
                Task.get_instructions(Task.triggers[serial_in][Task.state])
            except:
                #print('var1 probably not defined')
                pass

            '''
            try:
                #adds responses to arduino interrupts to output
                Calibrate.get_instructions(Calibrate.triggers[serial_in][Calibrate.state])
            #catch error if no line has been read
            except KeyError:
                print('No Key found')
            '''

            #writes output of processing onto output
            Task.update()

            #write outputs onto serial (in order!)
            for output in Task.output:
                write_serial(output,board)

            #turn any tasks on/off
            for control in Task.task_control:
                task_to_control = tasks_dict[control[0]]
                task_to_control.activate(control[1],control[2])

            #clear output
            Task.output = []
            Task.task_control = []

    #reset serial
    serial_in = ''

'''
Think about timing here, especailly in the write_serial loop. Perhaps some handshaking is required, etc...
Furthermore, serial_in could be modified to return a list of the most important triggers from the serial since the last reset of the loop
--> this would make the whol ething work regardless of the loop time
'''