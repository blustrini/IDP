'''
The main loop of the program
'''
#import modules
from serial_con import *
from task import *
from dim import *
from calibrate_dist import *
from navigate import *
from block_sort import *
from block_detect import *

#create board object
board = establish_serial(find_usb_port())

print('board')

#initialise dimension object
Dim = Dim()

#initialise tasks
Block_Sort = Block_Sort(Dim)
Block_Detect = Block_Detect(Dim)
Calibrate_Dist = Calibrate_Dist(Dim)
Navigate = Navigate(Dim)


#create list of tasks
tasks = [Calibrate_Dist,Navigate]
#create dict of tasks
task_dict = {
    'Calibrate_Dist':Calibrate_Dist,
    'Navigate':Navigate,
    'Block_Sort':Block_Sort,
    'Block_Detect':Block_Detect
}

Calibrate_Dist.active = 0
Navigate.active = 1
Block_Pickup.active = 1

# code to test serial input buffer working
# n = 10
# i = -1
#main loop
# while True:
#   i = i+1
#   i = i%10

#   if i != 0:
#       serial_in = read_next_line(board)
#       print('line: {}'.format(serial_in))

#   else:
#       print('buffer size: {}'.format(board.inWaiting()))
#       serial_in = flush_buffer(board)
#       for j in serial_in[1]:
#           print('line: {}'.format(j))   

#main loop
while True:
    #get serial input
    serial_in = read_next_line(board,decode=True,strip=True)
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