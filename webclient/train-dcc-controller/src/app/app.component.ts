import { Component } from '@angular/core';
import { LocoService } from './loco.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'train-dcc-controller';
  websocketIsConnected:boolean = false;
  addLocoTextfieldValue = null;

  constructor(private locoService: LocoService){
  }

  ngOnInit():void{
    this.locoService.getWebsocket().subscribe(
      {
        next: (v) =>  this.websocketIsConnected = true,
        error: (e) => this.websocketIsConnected = false,
        complete: () => console.info('app complete')
      }
    );
  }

  add():void{
    if (this.addLocoTextfieldValue && this.addLocoTextfieldValue < 10 && this.addLocoTextfieldValue > 0){
      this.locoService.send(this.asm_websocket_message("addLoco",{"address":this.addLocoTextfieldValue}));
    }
  }

  requestReset():void{
    this.locoService.send(this.asm_websocket_message("reset",{}));
  }

  reloadPage():void {
    window.location.reload();
  }

  asm_websocket_message(type:string, data:object): string{
    return JSON.stringify({"type": type, "data": data})

  }
}
