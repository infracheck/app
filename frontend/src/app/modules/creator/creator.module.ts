import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {CreatorComponent} from "./creator.component";
import {SharedModule} from "../shared.module";
import {CreatorRoutingModule} from './creator-routing.module';
import {TestWizard} from "./test-creator/test-wizard.component";
import {GeneralDataInputComponent} from "./general-data-input/general-data-input.component";
import {PluginDataInputComponent} from "./plugin-data-input/plugin-data-input.component";


@NgModule({
    declarations: [
        CreatorComponent,
        GeneralDataInputComponent,
        TestWizard,
        PluginDataInputComponent
    ],
    imports: [
        CommonModule,
        CreatorRoutingModule,
        SharedModule,
    ]
})
export class CreatorModule {
}
