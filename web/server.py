import signal
import socket
# import socket programming library
import socketwrapper
import serialwrapper
import messagebuilder

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

	ss:socketwrapper.Socket
	com:serialwrapper.Serial

	def socketread(client:socket.socket, read:str) -> bool:
		commendparts = read.strip().split(" ")
		msg = ""
		if commendparts[0] == 'S':
			msg = messagebuilder.speedcontrol(int(commendparts[1]), int(commendparts[2]), int(commendparts[3]))
		if commendparts[0] == 'F':
			msg = messagebuilder.functioncontrol(int(commendparts[1]), int(commendparts[2]), bool(int(commendparts[3])))
		print(msg)
		com.bufferwrite.put(msg)


	ss = socketwrapper.Socket("", 12345, callback_read = socketread)
	com = serialwrapper.Serial("COM10", 9600)

	# a forever loop until client wants to exit
	try:
		while True:
			line = input("?")
			com.bufferwrite.put(line)
	except ProgramInterrupted:
		pass
		#for x in threadslist:
	#		x.join()
	#s.close()
 
if __name__ == '__main__':
	main()