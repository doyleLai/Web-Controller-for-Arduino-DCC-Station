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
	
	def getlocos(self) -> list[loco.Loco]:
		return self.locos

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

	def serializer_loco(data: loco.Loco) -> str:
		_dict = {
			"type": "loco",
			"data": data
		}
		return json.dumps(_dict, cls=loco.LocoJSONEncode)

	def serializer_locos(data: list[loco.Loco]) -> str:
		_dict = {
			"type": "locos",
			"data": data
		}
		return json.dumps(_dict, cls=loco.LocoJSONEncode)

	def addLoco(clinet, server, data):
		if "address" in data:
			_addr = int(data["address"])
			if locoController.findLocoByAddress(_addr) == None:
				_loco = loco.Loco(_addr)
				locoController.add(_loco)
				print(f'Added a Loco with address {_addr}')
				com.bufferwrite.put(messagebuilder.speedcontrol_loco(_loco))
				ws.send_message_to_all(serializer_loco(_loco))

	def getLocos(clinet, server, data):
		_locos:list[loco.Loco] = locoController.getlocos()
		ws.send_message(clinet, serializer_locos(_locos))
	
	def c_speed(clinet, server, data):
		if "address" in data and "direction" in data and "speed" in data:
			_addr = int(data["address"])
			_new_dir = bool(int(data["direction"]))
			_new_speed = int(data["speed"])
			_loco = locoController.findLocoByAddress(_addr)
			if _loco != None:
				_loco.direction = _new_dir
				_loco.speed = _new_speed
				print(f'Loco address {_addr} has new direction {"UP" if _new_dir else "DN"} and speed {_new_speed}')
				com.bufferwrite.put(messagebuilder.speedcontrol_loco(_loco))
				ws.send_message_to_all(serializer_loco(_loco))

	def c_fun(clinet, server, data):
		if "address" in data and "function" in data and "isOn" in data:
			_addr = int(data["address"])
			_fun = int(data["function"])
			_isOn = bool(int(data["isOn"]))
			_loco = locoController.findLocoByAddress(_addr)
			if _loco != None and _fun < len(_loco.functions):
				_loco.functions[_fun].isOn = _isOn
				print(f'Loco address {_addr}\'s function {_fun} turns {"ON" if _isOn else "OFF"}')
				com.bufferwrite.put(messagebuilder.functioncontrol(_addr, _fun, _isOn))
				ws.send_message_to_all(serializer_loco(_loco))

	websocket_msg_handler.add_hanlder('addLoco', addLoco)
	websocket_msg_handler.add_hanlder('getLocos', getLocos)
	websocket_msg_handler.add_hanlder('c_speed', c_speed)
	websocket_msg_handler.add_hanlder('c_fun', c_fun)

	ws= WebsocketServer(host=host, port=port)
	ws.set_fn_message_received(socketread)
	#ss = socketwrapper.Socket("", 12345, callback_read = socketread)
	com = serialwrapper.Serial(serialport, 9600)
	print(f'Websocket listening on {host}:{port}')
	ws.run_forever(true)
	# a forever loop until client wants to exit
	try:
		while True:
			# add a default loco to the system when start 
			_loco = loco.Loco(3)
			locoController.add(_loco)
			print(f'Added a Loco with address {_loco.address}')
			com.bufferwrite.put(messagebuilder.speedcontrol_loco(_loco))

			line = input("> ")
			com.bufferwrite.put(line)
	except ProgramInterrupted:
		pass
		#for x in threadslist:
	#		x.join()
	#s.close()
 
if __name__ == '__main__':
	main()