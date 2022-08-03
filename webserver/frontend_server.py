import http.server
import socketserver
import os
import sys
import signal

PORT = 8000

class ProgramInterrupted(Exception):
	pass

def signal_handler(signum, frame):
	print(f'Signal {signum} received')
	raise ProgramInterrupted

def main():
	signal.signal(signal.SIGTERM, signal_handler)
	signal.signal(signal.SIGINT, signal_handler)

	web_dir = os.path.join(os.path.dirname(__file__), 'html')
	os.chdir(web_dir)

	Handler = http.server.SimpleHTTPRequestHandler
	httpd = socketserver.TCPServer(("", PORT), Handler)
	print("Serving HTTP at port", PORT)

	try:
		httpd.serve_forever()
	except ProgramInterrupted:
		sys.exit(0)
		#httpd.server_close()
		pass

if __name__ == '__main__':
	main()