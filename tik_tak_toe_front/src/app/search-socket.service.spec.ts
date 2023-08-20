import { TestBed } from '@angular/core/testing';

import { SearchSocketService } from './search-socket.service';

describe('SearchSocketService', () => {
  let service: SearchSocketService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SearchSocketService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
