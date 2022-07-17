import { Injectable } from '@angular/core';
import { Loco } from './loco';
import { Observable } from 'rxjs';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { LOCOS } from './locos-mock';

@Injectable({
  providedIn: 'root'
})

export class LocoService {
  private webSocket!: WebSocketSubject<any>;
  private URL:string = `ws://${window.location.hostname}:12345`;

  getLocos(): Loco[]{
    return LOCOS;
  }

  constructor() {
    this.connect();
  }
  
  getWebsocket():WebSocketSubject<any>{
    return this.webSocket;
  }

  connect(): Observable<any> {
    if (!this.webSocket || this.webSocket.closed) {
      console.log("connect");
      this.webSocket = webSocket({
        url:this.URL,
        deserializer: msg => msg,
        serializer: msg => msg.toString()
      });
      this.webSocket.subscribe(
        {
          next: (v) =>  console.log(v.data),
          error: (e) => {console.error(e)},
          complete: () => console.info('complete')
        }
      );
    }
    return this.webSocket
  }

  send(data: any) {
    if (this.webSocket) {
      console.log(data)
      this.webSocket.next(data);
    }
    else {
      console.error('Did not send data, open a connection first');
    }
  }

  closeConnection() {
    if (this.webSocket) {
      this.webSocket.complete();
      //this.myWebSocket$ = null;
    }
  }

  ngOnDestroy() {
    this.closeConnection();
  }
}
