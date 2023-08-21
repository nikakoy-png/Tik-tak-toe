import { TestBed } from '@angular/core/testing';

import { PlaySocketService } from './play-socket.service';

describe('PlaySocketService', () => {
  let service: PlaySocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PlaySocketService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
