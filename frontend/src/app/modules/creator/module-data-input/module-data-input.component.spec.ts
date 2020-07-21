import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleDataInputComponent } from './module-data-input.component';

describe('ModuleDataInputComponent', () => {
  let component: ModuleDataInputComponent;
  let fixture: ComponentFixture<ModuleDataInputComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModuleDataInputComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModuleDataInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
