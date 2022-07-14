import { Conditional } from '@angular/compiler';
import { Component, OnInit, Input } from '@angular/core';
import { Loco } from '../loco';
import { LocoService } from '../loco.service';

@Component({
  selector: 'app-loco-control',
  templateUrl: './loco-control.component.html',
  styleUrls: ['./loco-control.component.css']
})
export class LocoControlComponent implements OnInit {
  @Input() loco? : Loco
  constructor(private locoService: LocoService) { }

  ngOnInit(): void {
  }


  speedOnChanged(address:number, direction:boolean, speed:number):void{
    this.locoService.send(this.asm_message_c_speed(address, direction, speed));
  }

  functionOnChanged(address:number, index:number, isOn:boolean):void{
    this.locoService.send(this.asm_message_c_fun(address, index, !isOn));
  }

  asm_message_c_fun(address:number, index:number, isOn:boolean):string{
    return `{"type": "c_fun", "data": {"address":${address}, "function": ${index}, "isOn": ${isOn}}}`
  }

  asm_message_c_speed(address:number, direction:boolean, speed:number):string{
    return `{"type": "c_speed", "data": {"address":${address}, "direction":${direction}, "speed":${speed}}}`
  }


}
