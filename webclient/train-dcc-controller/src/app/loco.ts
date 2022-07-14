import { LocoFunction } from "./LocoFunction";

export interface Loco {
    address: number;
    dir: boolean;
    speed: number;
    func: LocoFunction[];

    /*
    constructor(address: number){
      this.address = address;
      this.dir = true;
      this.speed = 0;
      this.func = []
      for (let i = 0; i < 21; i++){
        this.func.push(new LocoFunction(i));
      }

    }
    */
}