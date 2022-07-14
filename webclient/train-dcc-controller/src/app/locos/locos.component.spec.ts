import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LocosComponent } from './locos.component';

describe('LocosComponent', () => {
  let component: LocosComponent;
  let fixture: ComponentFixture<LocosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ LocosComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LocosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
