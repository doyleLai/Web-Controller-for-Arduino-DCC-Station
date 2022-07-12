# Web-Controller-for-Arduino-DCC-Station
## Preliminary design of websocket message format and protocol
The socket server store the status of locos and broadcast the status to all clients periodically (maybe once every 5 sec). After receiving a change request from a client, the server broadcast the new state of that loco to all clients immediately.

### To server
- getLocos: ask server to send back the status of locos immedilately
- addLoco: add a new Loco in the server
- c_speed: change the speed of a loco
- c_fun: change a function state of a loco

### To client
- loco: notifly the current status of a loco
- locos: notifly the current status of locos

Messages are formated in JSON. 
|Type    |Example| 
|--------|-------|
|getLocos|{"type": "getLocos", "data": [{"address":3, "direction": 1, "speed": 0, "functions":[1,0,0,0,...]}, ...]}|
|addLoco |{"type": "addLoco", "data": {"address":3}}                                                               |
|c_speed |{"type": "c_speed", "data": {"address":3, "direction": 0, "speed": 127}}                                 |
|c_fun   |{"type": "c_speed", "data": {"address":3, "function": 10, "isOn": true}}                                 |
|loco    |{"type": "loco", "data": {"address":3, "direction": 1, "speed": 0, "functions":[1,0,0,0,...]}}           |
|locos   |{"type": "locos", "data": [{"address":3, "direction": 1, "speed": 0, "functions":[1,0,0,0,...]}, ...]}     |
