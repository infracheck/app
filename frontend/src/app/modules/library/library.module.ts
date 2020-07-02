import {NgModule} from '@angular/core';

import {SharedModule} from '../shared.module';
import {LibraryRoutingModule} from './library-routing.module';
import {LibraryComponent} from './library.component';


@NgModule({
  declarations: [
    LibraryComponent,
  ],
  imports: [
    LibraryRoutingModule,
    SharedModule,
  ]
})
export class LibraryModule {
}
