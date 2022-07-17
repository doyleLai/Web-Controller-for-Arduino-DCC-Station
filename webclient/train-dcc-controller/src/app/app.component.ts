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
}
