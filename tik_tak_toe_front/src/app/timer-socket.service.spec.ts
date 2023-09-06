import { TestBed } from '@angular/core/testing';

import { TimerSocketService } from './timer-socket.service';

describe('TimerSocketService', () => {
  let service: TimerSocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(TimerSocketService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
