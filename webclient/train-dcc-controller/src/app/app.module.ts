import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { LocosComponent } from './locos/locos.component';
import { LocoControlComponent } from './loco-control/loco-control.component';

@NgModule({
  declarations: [
    AppComponent,
    LocosComponent,
    LocoControlComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
