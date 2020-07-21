import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {CreatorComponent} from "./creator.component";
import {SharedModule} from "../shared.module";
import {CreatorRoutingModule} from './creator-routing.module';
import {TestWizard} from "./test-creator/test-wizard.component";
import {PluginDataInputComponent} from "./plugin-data-input/plugin-data-input.component";
import {ModuleDataInputComponent} from "./module-data-input/module-data-input.component";


@NgModule({
    declarations: [
        CreatorComponent,
        TestWizard,
        PluginDataInputComponent,
        ModuleDataInputComponent
    ],
    imports: [
        CommonModule,
        CreatorRoutingModule,
        SharedModule,
    ]
})
export class CreatorModule {
}
