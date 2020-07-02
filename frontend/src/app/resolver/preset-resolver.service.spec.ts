import {TestBed} from '@angular/core/testing';

import {PresetResolverService} from './preset-resolver.service';

describe('PresetResolverService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: PresetResolverService = TestBed.get(PresetResolverService);
    expect(service).toBeTruthy();
  });
});
