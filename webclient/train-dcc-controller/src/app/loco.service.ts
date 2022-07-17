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

  getLocos(): Loco[]{
    return LOCOS;
  }

  constructor() {
    this.connect(`ws://${window.location.hostname}:12345`);
  }
  
  getWebsocket():WebSocketSubject<any>{
    return this.webSocket;
  }

  connect(url:string): Observable<any> {
    if (!this.webSocket || this.webSocket.closed) {
      console.log("connect");
      this.webSocket = webSocket({
        url:url,
        deserializer: msg => msg,
        serializer: msg => msg.toString()
      });
      this.webSocket.subscribe(
        {
          next: (v) =>  console.log(v.data),
          error: (e) => console.error(e),
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
