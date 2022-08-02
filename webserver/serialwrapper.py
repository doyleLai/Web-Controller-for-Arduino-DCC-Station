import queue
from typing import Callable, List
import serial
import serial.tools.list_ports
import time
import threading

class Serial():
	port:str = None
	buadrate:int = None
	serialPortVerification:Callable[[str],bool] = None
	bufferread:queue.Queue = queue.Queue()
	bufferwrite:queue.Queue = queue.Queue()
	readHandler:Callable[[str], None] = None
	ser:serial.Serial = serial.Serial()
	entry:threading.Lock
	isRunning:bool = None

	def __init__(self, port:str = None, buadrate:int = None, verificationFunc:Callable[[str],bool] = None):
		self.port = port
		self.buadrate = buadrate
		self.serialPortVerification = verificationFunc
		self.connect()
		self.entry = threading.Lock()
		threadread = threading.Thread(target=self.worker_read, daemon=True).start()
		threadwrite = threading.Thread(target=self.worker_write, daemon=True).start()

	def connect(self):
		if self.port and self.buadrate:
			print(f'Connecting to {self.port}...')
			self.ser = serial.Serial(self.port, self.buadrate)
			print(f'Connected to {self.port}')
			#self.isRunning = True
		else:
			print("Searching for serial device...")
			s:serial.Serial = findPort(self.serialPortVerification)
			if s:
				self.ser = s
				self.ser.open()
				print(f'Connected to {s.port}')
				#self.isRunning = True
			else:
				print("Device not found")
		self.isRunning = True

	def reconnect(self):
		self.entry.acquire()
		time.sleep(2)
		try:
			if self.ser.is_open:
				print("isopen")
			elif self.port and self.buadrate:
				print(f'Reconnecting to {self.port}...')
				self.ser = serial.Serial(self.port, self.buadrate)
				print(f'Connected to {self.port}')
			else:
				print("Searching for serial device...")
				s:serial.Serial = findPort(self.serialPortVerification)
				if s:
					self.ser = s
					self.ser.open()
					print(f'Connected to {s.port}')
					self.isRunning = True
				else:
					print("Device not found")
		finally:
			self.entry.release()

	def worker_read(self):
		while self.isRunning:
			try:
				if self.ser.is_open:
					line = str(self.ser.readline().decode('utf-8').strip())
					if self.readHandler != None:
						self.readHandler(line)
					else:
						print(f'COM Read: {line}')
				else:
					self.reconnect()
			except serial.SerialException as e:
				print("An exception occurred when connecting COM:", e)
				self.ser.close()
			except Exception as e:
				print("Unknown exception when reading from COM.", e)
		self.ser.close()

	def worker_write(self):
		while self.isRunning:
			try:
				if self.ser.is_open:
					if self.bufferwrite.qsize():
						self.ser.write(bytes(self.bufferwrite.get(), encoding='ascii'))
				else:
					self.reconnect()
			except serial.SerialException as e:
				print("An exception occurred when connecting COM:", e)
				self.ser.close()
			except Exception as e:
				print("Unknown exception when writing to COM.", e)
		self.ser.close()

def listport() -> List:
	return serial.tools.list_ports.comports()

def findPort(verificationFunction) -> serial.Serial:
	ports = serial.tools.list_ports.comports()
	for port in ports:
		try:
			s:serial.Serial = serial.Serial(port.device, 9600 ,timeout=2)
			line = ""
			if s.is_open:
				line = str(s.readline().decode('utf-8').strip())
			s.close()
			if verificationFunction(line):
				s.timeout = None
				return s
		except (OSError, serial.SerialException):
			pass
	return None