import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PluginDataInputComponent } from './plugin-data-input.component';

describe('PluginDataInputComponent', () => {
  let component: PluginDataInputComponent;
  let fixture: ComponentFixture<PluginDataInputComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PluginDataInputComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PluginDataInputComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
