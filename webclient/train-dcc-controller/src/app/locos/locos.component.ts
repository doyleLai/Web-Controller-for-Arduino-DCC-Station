import { Component, OnInit } from '@angular/core';
import { Loco } from '../loco'
import { LocoService } from '../loco.service';
import { LocoFunction } from '../LocoFunction';

@Component({
  selector: 'app-locos',
  templateUrl: './locos.component.html',
  styleUrls: ['./locos.component.css']
})
export class LocosComponent implements OnInit {
  locos: Loco[] = [];
  constructor(private locoService: LocoService) { }

  ngOnInit(): void {
    //this.locos = this.locoService.getLocos()
    //.connect(`ws://${window.location.hostname}:12345`)
  
    this.locoService.getWebsocket().subscribe(msg => {
      let _obj = JSON.parse(msg.data);
      if (_obj.type == "locos"){
        let _locos: Loco[] = [];
        for (let l of _obj.data){
          _locos.push(this.jsonToType(l))
        }
        this.locos = _locos
      }
      else if (_obj.type == "loco"){
        let locoData = _obj.data;
        this.updateExistLoco(this.jsonToType(locoData));
      }
    });
  

    this.locoService.send(JSON.stringify({"type": "getLocos", "data": {}}
    ))
    
  }

  jsonToType(locoJson:any):Loco{
    let _address:number = locoJson.address;
    let _direction:boolean = locoJson.direction;
    let _speed:number = locoJson.speed;
    let _func:LocoFunction[] = [];
    for (let i = 0 ; i < locoJson.functions.length; i++) {
      _func.push({
        index: i,
        isOn: Boolean(locoJson.functions[i])
      });
    }

    let loco:Loco = {
      address: _address,
      dir: _direction,
      speed: _speed,
      func: _func
    };

    return loco;
  }
  
  findLocoByAddress(address:number):Loco|undefined{
    for (let l of this.locos){
      if (l.address==address){
        return l;
      }
    }
    return undefined;
  }

  updateExistLoco(locoData:Loco):void{
    let _address = locoData.address;
    for (let i = 0; i < this.locos.length; i++){
      if (this.locos[i].address == _address){
        Object.assign( this.locos[i], locoData)
        //this.locos[i].address = locoData.address;
        //this.locos[i].dir = locoData.dir;
        //this.locos[i].speed = locoData.speed;
      }
    }
  }

  send(data:string):void{
    this.locoService.send(data);
  }

}
