import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TestBuilderPresetsComponent} from './test-builder-presets.component';

describe('TestBuilderPresetsComponent', () => {
  let component: TestBuilderPresetsComponent;
  let fixture: ComponentFixture<TestBuilderPresetsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TestBuilderPresetsComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestBuilderPresetsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
