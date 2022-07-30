import queue
from tkinter.messagebox import NO
from typing import Callable
import serial as s
import time
import threading

class Serial():
	port:str = None
	buadrate:int = None
	bufferread:queue.Queue = queue.Queue()
	bufferwrite:queue.Queue = queue.Queue()
	readHandler:Callable[[str], None] = None
	ser:s.Serial = s.Serial()
	entry:threading.Lock
	isRunning:bool = None

	def __init__(self, port:str, buadrate:int):
		self.port = port
		self.buadrate = buadrate
		self.connect()
		threadread = threading.Thread(target=self.worker_read, daemon=True).start()
		threadwrite = threading.Thread(target=self.worker_write, daemon=True).start()
		self.entry = threading.Lock()
	
	def connect(self):
		print(f'Connecting to {self.port}...')
		self.ser = s.Serial(self.port, self.buadrate)
		print(f'Connected to {self.port}')
		self.isRunning = True

	def reconnect(self):
		self.entry.acquire()
		try:
			if self.ser.is_open:
				print("isopen")
			else:
				print(f'Reconnecting to {self.port}...')
				time.sleep(2)
				self.ser = s.Serial(self.port, self.buadrate)
				print(f'Connected to {self.port}')
				time.sleep(2)
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
			except s.SerialException as e:
				print("An exception occurred when connecting COM:", e)
				self.ser.close()
				time.sleep(2)
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
			except s.SerialException as e:
				print("An exception occurred when connecting COM:", e)
				self.ser.close()
				time.sleep(2)
			except Exception as e:
				print("Unknown exception when writing to COM.", e)
		self.ser.close()