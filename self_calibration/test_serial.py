import glob
import serial

ports = glob.glob('/dev/tty.*')

for port in ports:
	if 'MALS' in port:
		print(port)
		break
'''

serial_ports = []

ports = glob.glob('/dev/tty.*')

for port in ports:
	try:
		s = serial.Serial(port)
		s.close()
		print('success: {}'.format(port))
		serial_ports.append(port)
	except (OSError, serial.SerialException):
		print('error: {}'.format(port))


if __name__ == '__main__':
    print(serial_ports)
    '''