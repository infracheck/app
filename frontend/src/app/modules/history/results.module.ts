import {NgModule} from '@angular/core';
import {ResultsRoutingModule} from './results-routing.module';
import {ResultsComponent} from './results.component';
import {SharedModule} from '../shared.module';
import {CommonModule} from '@angular/common';


@NgModule({
  declarations: [
    ResultsComponent,
  ],
  imports: [
    ResultsRoutingModule,
    SharedModule,
    CommonModule
  ]
})
export class ResultsModule {
}
