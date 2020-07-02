import {TestBed} from '@angular/core/testing';

import {TestResolver} from './test-resolver.service';

describe('TestsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: TestResolver = TestBed.get(TestResolver);
    expect(service).toBeTruthy();
  });
});
