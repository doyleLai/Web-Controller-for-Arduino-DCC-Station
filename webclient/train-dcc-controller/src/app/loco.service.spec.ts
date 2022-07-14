import { TestBed } from '@angular/core/testing';

import { LocoService } from './loco.service';

describe('LocoService', () => {
  let service: LocoService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LocoService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
