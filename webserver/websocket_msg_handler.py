import json
from typing import Callable

handlers:dict[str, Callable] = {}

def add_hanlder(type:str, function:Callable) -> None:
    handlers[type] = function

def handle(client, server, msg:str) -> None:
    #print("handle:", msg)
    try:
        d = json.loads(msg)
        if 'type' in d and 'data' in d and d['type'] in handlers:
            handlers[d['type']](client, server, d['data'])
    except json.decoder.JSONDecodeError as e:
        print("Message does not look like a JSON string.", e)
    except ValueError as e:
        print("Some values in the message are not in correct format.", e)
