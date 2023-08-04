from multiprocessing import Process
import sys
import os
import server
import frontend_server
import signal

class ProgramInterrupted(Exception):
	pass

def signal_handler(signum, frame):
	print(f'Signal {signum} received')
	raise ProgramInterrupted

def info(title):
	print(title)
	print('module name:', __name__)
	print('parent process:', os.getppid())
	print('process id:', os.getpid())

def main():
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)

	info('main line')
	if len(sys.argv) == 3:
		p1 = Process(target=server.main, args=(), kwargs={"serialport":sys.argv[1], "baudrate":int(sys.argv[2])})
	else:
		p1 = Process(target=server.main, args=())
	p2 = Process(target=frontend_server.main, args=(), daemon=True)
	p1.start()
	p2.start()
	try:
		p1.join()
	except ProgramInterrupted as e:
		print("Terminating process")
		p1.terminate()
		p2.terminate()
	#p2.join()
	print("Web controller terminated")

if __name__ == '__main__':
	print((f'The name of the serial port to connect the Arduino can be given. In this case, baudrate should also be given.\n'
			f'Example:\n'
			f'{sys.argv[0]} /dev/ttyS0 9600\n'
			f'If no serial port name is given, the program will search for the device on available ports.\n'
			) ,file=sys.stderr)
	main()