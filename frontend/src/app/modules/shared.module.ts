import {NgModule} from '@angular/core';
import {ClarityModule} from '@clr/angular';

import {ResultViewComponent} from '../components/result-view/result-view.component';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {PresetPreviewComponent} from '../components/preset-preview/preset-preview.component';
import {TestNamePipe} from '../services/test-name.pipe';
import {TestSettingsModalComponent} from '../components/test-settings-modal/test-settings-modal.component';
import {MarkdownModule} from 'ngx-markdown';
import {TestEditorComponent} from '../components/test-builder-editor/test-editor.component';
import {TestSearchPipe} from '../services/test-search.pipe';
import {TestPreviewComponent} from '../components/test-preview/test-preview.component';


@NgModule({
  declarations: [
    PresetPreviewComponent,
    ResultViewComponent,
    TestNamePipe,
    TestSettingsModalComponent,
    TestEditorComponent,
    TestSearchPipe,
    TestPreviewComponent
  ],
  imports: [
    ClarityModule,
    HttpClientModule,
    FormsModule,
    CommonModule,
    MarkdownModule.forRoot(),
  ],
  exports: [
    ClarityModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    CommonModule,
    PresetPreviewComponent,
    ResultViewComponent,
    MarkdownModule,
    TestSettingsModalComponent,
    TestEditorComponent
  ],
  providers: []
})
export class SharedModule {
}
