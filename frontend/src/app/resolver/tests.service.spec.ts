import {TestBed} from '@angular/core/testing';

import {PluginResolver} from './test-resolver.service';

describe('TestsService', () => {
    beforeEach(() => TestBed.configureTestingModule({}));

    it('should be created', () => {
        const service: PluginResolver = TestBed.get(PluginResolver);
        expect(service).toBeTruthy();
    });
});
