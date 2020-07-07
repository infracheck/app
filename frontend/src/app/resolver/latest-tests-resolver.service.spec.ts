import {TestBed} from '@angular/core/testing';

import {LatestTestsResolverService} from './latest-tests-resolver.service';

describe('LatestTestsResolverService', () => {
    beforeEach(() => TestBed.configureTestingModule({}));

    it('should be created', () => {
        const service: LatestTestsResolverService = TestBed.get(LatestTestsResolverService);
        expect(service).toBeTruthy();
    });
});
