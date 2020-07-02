import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TestSettingsModalComponent} from './test-settings-modal.component';

describe('TestSettingsModalComponent', () => {
  let component: TestSettingsModalComponent;
  let fixture: ComponentFixture<TestSettingsModalComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TestSettingsModalComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestSettingsModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
