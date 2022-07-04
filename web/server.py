import signal
# import socket programming library
import socketwrapper

# Things to implememt:
#	Message factory
#	Message buffer
#	Serial writer
#	Layout - storing layout status (Locos, speeds, function on/off, etc...) ?

class ProgramInterrupted(Exception):
	pass

def signal_handler(signum, frame):
	print(f'Signal {signum} received')
	raise ProgramInterrupted

def main():
	print("Service started")
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)

	ss = socketwrapper.Socket("", 12345)

	# a forever loop until client wants to exit
	try:
		while True:
			pass
	except ProgramInterrupted:
		pass
		#for x in threadslist:
	#		x.join()
	#s.close()
 
if __name__ == '__main__':
	main()