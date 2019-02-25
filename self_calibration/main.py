'''
The main loop of the program
'''
#import modules
from serial_con import *
from task import *
from dim import *


#create board object
board = establish_serial(find_usb_port())

print('board')

#initialise dimension object
Dim = Dim()
#initialise progress object
Calibrate = Calibrate(Dim)


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

    

while True:
    serial_in = read_next_line(board,decode=True,strip=True)
    if serial_in != None:
        print(serial_in)
    #feed line into task object
    try:
        key1 = Calibrate.triggers[serial_in]
    except:
        #print('Key: {} not found in triggers dict'.format(serial_in))
        pass

    try:
        var1 = key1[Calibrate.state]
    except:
        #print('Key: \'{}\' not found in triggers dict'.format(Calibrate.state))
        pass

    try:
        Calibrate.get_instructions(var1)
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
    #adds output of processin gonto output
    Calibrate.update()

    #write all instructions to serial, DATA STRUCTURE NEEDS RETHINKING!
    #print(Calibrate.output)
    for i in Calibrate.output:
        write_serial(i,board)

    Calibrate.output = []
    var1,key1 = None,None

    serial_in = ''

'''
Think about timing here, especailly in the write_serial loop. Perhaps some handshaking is required, etc...
Furthermore, serial_in could be modified to return a list of the most important triggers from the serial since the last reset of the loop
--> this would make the whol ething work regardless of the loop time
'''