from multiprocessing import Process
import os
import server
import frontend_server
import signal

#class ProgramInterrupted(Exception):
#	pass

def signal_handler(signum, frame):
	print(f'Signal {signum} received')
	#raise ProgramInterrupted

def info(title):
	print(title)
	print('module name:', __name__)
	print('parent process:', os.getppid())
	print('process id:', os.getpid())


if __name__ == '__main__':
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)

	info('main line')
	p1 = Process(target=server.main, args=())
	p2 = Process(target=frontend_server.main, args=(), daemon=True)
	p1.start()
	p2.start()
	p1.join()
	#p2.join()
	print("Web controller terminated")