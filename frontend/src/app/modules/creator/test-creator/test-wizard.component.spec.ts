import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TestWizard} from './test-wizard.component';

describe('TestCreatorComponent', () => {
    let component: TestWizard;
    let fixture: ComponentFixture<TestWizard>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            declarations: [TestWizard]
        })
            .compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(TestWizard);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
