import {NgModule} from '@angular/core';

import {SharedModule} from '../shared.module';
import {DocumentationRoutingModule} from './documentation-routing.module';
import {DocumentationComponent} from './documentation.component';
import {MarkdownModule} from 'ngx-markdown';
import {CommonModule} from '@angular/common';


@NgModule({
    declarations: [
        DocumentationComponent,
    ],
    imports: [
        CommonModule,
        DocumentationRoutingModule,
        SharedModule,
        MarkdownModule.forRoot()
    ]
})
export class DocumentationModule {
}
