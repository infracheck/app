import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneralDataInputComponent } from './general-data-input.component';

describe('GeneralDataInputComponent', () => {
  let component: GeneralDataInputComponent;
  let fixture: ComponentFixture<GeneralDataInputComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ GeneralDataInputComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneralDataInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
