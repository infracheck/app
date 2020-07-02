import {NgModule} from '@angular/core';

import {SharedModule} from '../shared.module';
import {StartComponent} from './start.component';
import {StartRoutingModule} from './start-routing.module';
import {TestBuilderMetaDataComponent} from './test-builder-meta-data/test-builder-meta-data.component';
import {TestBuilderPresetsComponent} from './test-builder-presets/test-builder-presets.component';
import {DocumentationModule} from '../documentation/documentation.module';


@NgModule({
  declarations: [
    StartComponent,
    TestBuilderMetaDataComponent,
    TestBuilderPresetsComponent
  ],
  imports: [
    StartRoutingModule,
    SharedModule,
    DocumentationModule,
  ],
  exports: [
  ],
  providers: []
})
export class StartModule {
}
