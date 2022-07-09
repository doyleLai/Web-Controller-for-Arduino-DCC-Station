from typing import Callable
from websocket_server import WebsocketServer

class Websocket():
    def _init_(self, host:str, port:int):
        self.ws = WebsocketServer(host = host, port = port)

    def set_fn_msg_received(self, func:Callable):
        self.ws.set_fn_message_received(func)
    
    def start(self):
        self.ws.run_forever()