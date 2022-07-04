import serial as s
import time

class Serial():
	port:str = None
	buadrate:int = None
	ser:s.Serial = s.Serial()
	isRunning:bool = None

	def __init__(self, port:str, buadrate:int):
		self.port = port
		self.buadrate = buadrate
		print(f'Connecting to {port}...')
		self.ser = s.Serial(port, buadrate)
		print(f'Connected to {port}')
		self.isRunning = True

	def threadread(self):
		while self.isRunning:
			try:
				if self.ser.is_open:
					line = str(self.ser.readline().decode('utf-8').strip())
					print(line)
				else:
					print(f'Reconnecting to {self.port}...')
					time.sleep(2)
					self.ser = s.Serial(self.port, self.buadrate)
					print(f'Connected to {self.port}')
			except s.SerialException as e:
				print("An exception occurred when connecting COM:", e)
				self.ser.close()
				time.sleep(2)
			except Exception as e:
				print("Unknown exception.", e)
		self.ser.close()