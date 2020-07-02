import {async, ComponentFixture, TestBed} from '@angular/core/testing';

import {PresetPreviewComponent} from './preset-preview.component';

describe('LibraryPreviewComponent', () => {
  let component: PresetPreviewComponent;
  let fixture: ComponentFixture<PresetPreviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [PresetPreviewComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PresetPreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
