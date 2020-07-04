import {NgModule} from '@angular/core';
import {CommonModule} from '@angular/common';
import {CreatorComponent} from "./creator.component";
import {SharedModule} from "../shared.module";
import {CreatorRoutingModule} from './creator-routing.module';



@NgModule({
    declarations: [
        CreatorComponent
    ],
    imports: [
        CommonModule,
        CreatorRoutingModule,
        SharedModule
    ]
})
export class CreatorModule {
}
