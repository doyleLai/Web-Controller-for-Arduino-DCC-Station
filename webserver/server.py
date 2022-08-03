import sys
import json
import signal
from time import sleep
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

	def reset(self) -> None:
		self.locos = []



class ProgramInterrupted(Exception):
	pass

def signal_handler(signum, frame):
	print(f'Signal {signum} received')
	raise ProgramInterrupted


def main(serialport:str = None, host:str = "", port:int = 12345):
	print("Service started")
	
	locoController = LocosController()

	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)

	ws:WebsocketServer
	#ss:socketwrapper.Socket
	serial:serialwrapper.Serial

	# ========================================
	# Helper functions used in other functions
	# ========================================

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

	# ======================
	# Handlers for websocket
	# ======================
	
	def socketread(client, server, read) -> None:
		websocket_msg_handler.handle(client, server, read)

	def ws_addLoco(clinet, server, data):
		if "address" in data:
			_addr = int(data["address"])
			if locoController.findLocoByAddress(_addr) == None:
				_loco = loco.Loco(_addr)
				locoController.add(_loco)
				print(f'Added a Loco with address {_addr}')
				serial.bufferwrite.put(messagebuilder.speedcontrol_loco(_loco))
				ws.send_message_to_all(serializer_loco(_loco))

	def ws_getLocos(clinet, server, data):
		_locos:list[loco.Loco] = locoController.getlocos()
		ws.send_message(clinet, serializer_locos(_locos))
	
	def ws_c_speed(clinet, server, data):
		if "address" in data and "direction" in data and "speed" in data:
			_addr = int(data["address"])
			_new_dir = bool(int(data["direction"]))
			_new_speed = int(data["speed"])
			_loco = locoController.findLocoByAddress(_addr)
			if _loco != None:
				_loco.direction = _new_dir
				_loco.speed = _new_speed
				print(f'Loco address {_addr} has new direction {"UP" if _new_dir else "DN"} and speed {_new_speed}')
				serial.bufferwrite.put(messagebuilder.speedcontrol_loco(_loco))
				ws.send_message_to_all(serializer_loco(_loco))

	def ws_c_fun(clinet, server, data):
		if "address" in data and "function" in data and "isOn" in data:
			_addr = int(data["address"])
			_fun = int(data["function"])
			_isOn = bool(int(data["isOn"]))
			_loco = locoController.findLocoByAddress(_addr)
			if _loco != None and _fun < len(_loco.functions):
				_loco.functions[_fun].isOn = _isOn
				print(f'Loco address {_addr}\'s function {_fun} turns {"ON" if _isOn else "OFF"}')
				serial.bufferwrite.put(messagebuilder.functioncontrol_loco(_loco, _fun))
				ws.send_message_to_all(serializer_loco(_loco))

	def ws_reset(clinet, server, data):
		serial.bufferwrite.put("<W>")

	websocket_msg_handler.add_hanlder('addLoco', ws_addLoco)
	websocket_msg_handler.add_hanlder('getLocos', ws_getLocos)
	websocket_msg_handler.add_hanlder('c_speed', ws_c_speed)
	websocket_msg_handler.add_hanlder('c_fun', ws_c_fun)
	websocket_msg_handler.add_hanlder('reset', ws_reset)

	# ========================
	# Handlers for serial port
	# ========================


	def serial_read(line:str):
		if line == "DCC_begin":
			print(line)

			locoController.reset()
			
			# add a default loco to the system when start 
			_loco = loco.Loco(3)
			locoController.add(_loco)
			print(f'Added a Loco with address {_loco.address}')
			serial.bufferwrite.put(messagebuilder.speedcontrol_loco(_loco))

			_locos:list[loco.Loco] = locoController.getlocos()
			ws.send_message_to_all(serializer_locos(_locos))

		else:
			print(line)
	
	def serialPortVerification(msg:str) -> bool:
		return msg == "DCC_begin"

	ws= WebsocketServer(host=host, port=port)
	ws.set_fn_message_received(socketread)
	#ss = socketwrapper.Socket("", 12345, callback_read = socketread)
	#serial = serialwrapper.Serial(serialport, 9600)
	serial = serialwrapper.Serial(verificationFunc=serialPortVerification)
	serial.readHandler = serial_read
	print(f'Websocket listening on {host}:{port}')
	ws.run_forever(True)
	# a forever loop until client wants to exit


	try:
		while True:
			if __name__ ==  '__main__':
				line = input("> ")
				serial.bufferwrite.put(line)
			else:
				sleep(1)
	except ProgramInterrupted:
		serial.close()
		ws.shutdown()
		#for x in threadslist:
	#		x.join()
	#s.close()
 
if __name__ == '__main__':
	main()
	"""
	if len(sys.argv) == 2:
		main(serialport = sys.argv[1])
	elif len(sys.argv) == 3:
		main(serialport = sys.argv[1], port=int(sys.argv[2]))
	else:
		print((f'{sys.argv[0]}: Serial port should be given. Websocket port can be given\n'
			f'Example:\n'
			f'{sys.argv[0]} COM10 12345\n'
			f'If no websocket port is given, default value port number 12345 will be used.\n'
			f'Available serial ports:'
		) ,file=sys.stderr)
		for p in sorted(serialwrapper.listport()):
				print(f'{p.device}: {p.description}')
	"""