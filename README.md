# Web-Controller-for-Arduino-DCC-Station
## Preliminary design of websocket message format
 The socket server store the status of locos and broadcast the status to all clients periodically (maybe once every 5 sec). 
### To server
- getLocos: server reply the status of locos immedilately
- c_speed: change the speed of a loco
- c_fun: change a function state of a loco
### To client
- locos: notifly the current status of locos
- n_speed: notifly the change of a loco's speed 
- n_fun: notifly the change of a loco's function state
