import { Loco } from "./loco";

let _LOCOS: Loco[] = [
   {
      address: 3,
      dir: false, 
      speed: 0,
      func:[
         {index:0, isOn:true},
         {index:1, isOn:false},
         {index:2, isOn:false},
         {index:3, isOn:false},
         {index:4, isOn:false},
         {index:5, isOn:false},
         {index:6, isOn:false},
         {index:7, isOn:false},
         {index:8, isOn:false},
         {index:9, isOn:false}
      ]
   },
   {
      address: 5,
      dir: false, 
      speed: 0,
      func:[
         {index:0, isOn:false},
         {index:1, isOn:false},
         {index:2, isOn:false},
         {index:3, isOn:false},
         {index:4, isOn:false},
         {index:5, isOn:false},
         {index:6, isOn:false},
         {index:7, isOn:false},
         {index:8, isOn:false},
         {index:9, isOn:false}
      ]
   }

];

export const LOCOS: Loco[] = _LOCOS