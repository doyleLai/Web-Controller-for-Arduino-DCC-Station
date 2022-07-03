from logging import exception
import socket

# import thread module
#from _thread import *
import threading

class SafeThread(threading.Thread):
	def __init__(self, execute, args=()):
		threading.Thread.__init__(self)
		self.stopped = threading.Event()
		self.execute = execute
		self.args = args
		self.is_first_ended = False
	
	def stop(self):
				self.stopped.set()
				self.join()
	def run(self):
			while not self.stopped.is_set():
				self.execute(*self.args)
			print("Thread exiting")

class Socketserver():
	new_connection_thread:threading.Thread = None
	threadslist:list[SafeThread] = []

	def __init__(self):
		host = ""
		# reverse a port on your computer
		# in our case it is 12345 but it
		# can be anything
		port = 12345
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		print("socket binded to port", port)
	
		# put the socket into listening mode
		s.listen(5)
		print("socket is listening")

		thread = threading.Thread(target = self.wait_connection, args=(s,))
		thread.daemon = True
		thread.start()
		self.new_connection_thread = thread
	
	def wait_connection(self, s: socket.socket):
		while True:
			# establish connection with client
			c, addr = s.accept()
			# lock acquired by client
			#print_lock.acquire()
			print('Connected to :', addr[0], ':', addr[1])

			# Start a new thread and return its identifier
			thread = threading.Thread(target = self.client_handler, args = (c,))
			thread.start()
			#self.threadslist.append(thread)

	def client_handler(self, c):
		while True:
			try:
				# data received from client
				data = c.recv(1024)
				if not data:
					print('Bye')
					
					# lock released on exit
					#print_lock.release()
					break
		
				# reverse the given string from client
		
				# send back reversed string to client
				print(data)
				c.send(data)
			except ConnectionResetError as e:
				break
			except Exception as e:
				print("Unknown error:", e)
	
		# connection closed
		print("Client closed.")
		c.close()
	
	def broadcast(self, msg:str):
		print(msg)

# thread function

 


