import {NgModule} from '@angular/core';
import {ClarityModule} from '@clr/angular';

import {ResultViewComponent} from '../components/result-view/result-view.component';
import {HttpClientModule} from '@angular/common/http';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {CommonModule} from '@angular/common';
import {TestNamePipe} from '../services/test-name.pipe';
import {MarkdownModule} from 'ngx-markdown';
import {TestSearchPipe} from '../services/test-search.pipe';
import {DynamicFormElementComponent} from "../components/dynamic-form-element/dynamic-form-element.component";


@NgModule({
    declarations: [
        ResultViewComponent,
        TestNamePipe,
        TestSearchPipe,
        DynamicFormElementComponent
    ],
    imports: [
        ClarityModule,
        HttpClientModule,
        FormsModule,
        CommonModule,
        MarkdownModule.forRoot()
    ],
    exports: [
        ClarityModule,
        HttpClientModule,
        FormsModule,
        ReactiveFormsModule,
        CommonModule,
        ResultViewComponent,
        MarkdownModule,
        DynamicFormElementComponent
    ],
    providers: []
})
export class SharedModule {
}
