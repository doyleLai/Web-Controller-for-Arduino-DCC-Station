from audioop import add
import json
import signal

from sqlalchemy import true
#import socket
# import socket programming library
#import socketwrapper
import serialwrapper
import DCC.messagebuilder as messagebuilder
import DCC.loco as loco
from websocket_server import WebsocketServer
import websocket_msg_handler

# Things to implememt:
#	Message factory
#	Message buffer
#	Serial writer
#	Layout - storing layout status (Locos, speeds, function on/off, etc...) ?


class LocosController:
	def __init__(self) -> None:
		self.locos:list[loco.Loco] = []

	def add(self, loco:loco.Loco) -> None:
		self.locos.append(loco)
	
	def findLocoByAddress(self, address:int) -> loco.Loco:
		for _loco in self.locos:
			if _loco.address == address:
				return _loco
		return None



class ProgramInterrupted(Exception):
	pass

def signal_handler(signum, frame):
	print(f'Signal {signum} received')
	raise ProgramInterrupted


def main(host:str = "127.0.0.1", port:int = 12345, serialport:str = "COM10"):
	print("Service started")
	
	locoController = LocosController()

	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)

	ws:WebsocketServer
	#ss:socketwrapper.Socket
	com:serialwrapper.Serial

	def socketread(client, server, read) -> None:
		#print("socketread:", read)
		websocket_msg_handler.handle(client, server, read)
		"""
		ws.send_message(client, "ok")
		commendparts = read.strip().split(" ")
		msg = ""
		if commendparts[0] == 'S':
			msg = messagebuilder.speedcontrol(int(commendparts[1]), int(commendparts[2]), int(commendparts[3]))
		if commendparts[0] == 'F':
			msg = messagebuilder.functioncontrol(int(commendparts[1]), int(commendparts[2]), bool(int(commendparts[3])))
		print(msg)
		com.bufferwrite.put(msg)
		"""

	def addLoco(clinet, server, data):
		if "address" in data:
			_addr = int(data["address"])
			if locoController.findLocoByAddress(_addr) == None:
				locoController.add(loco.Loco(_addr))
				print(f'Added a Loco with address {_addr}')
				_loco = locoController.findLocoByAddress(_addr)
				ws.send_message_to_all(json.dumps(_loco, cls=loco.LocoJSONEncode))

	websocket_msg_handler.add_hanlder('addLoco', addLoco)

	ws= WebsocketServer(host=host, port=port)
	ws.set_fn_message_received(socketread)
	#ss = socketwrapper.Socket("", 12345, callback_read = socketread)
	com = serialwrapper.Serial(serialport, 9600)
	print(f'Websocket listening on {host}:{port}')
	ws.run_forever(true)
	# a forever loop until client wants to exit
	try:
		while True:
			line = input("> ")
			com.bufferwrite.put(line)
	except ProgramInterrupted:
		pass
		#for x in threadslist:
	#		x.join()
	#s.close()
 
if __name__ == '__main__':
	main()