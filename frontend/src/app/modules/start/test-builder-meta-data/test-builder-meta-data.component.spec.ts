import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {TestBuilderMetaDataComponent} from './test-builder-meta-data.component';

describe('TestBuilderMetaDataComponent', () => {
  let component: TestBuilderMetaDataComponent;
  let fixture: ComponentFixture<TestBuilderMetaDataComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [TestBuilderMetaDataComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestBuilderMetaDataComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
