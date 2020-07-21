import {Component, Input, OnInit} from '@angular/core';
import {ApiInputModuleData, ApiModule} from "../../../definitions/api";

@Component({
    selector: 'app-module-data-input',
    templateUrl: './module-data-input.component.html',
    styleUrls: ['./module-data-input.component.scss']
})
export class ModuleDataInputComponent implements OnInit {

    @Input() moduleData: ApiInputModuleData[];
    @Input() moduleDefinitions: ApiModule[];
    selected: any;

    constructor() {
    }

    ngOnInit(): void {
    }

    addModule(module: ApiModule) {
        this.moduleData.push({
            id: module.id,
            fields: {}
        })
    }

    getDefinedModuleFields(id: string) {
        return this.moduleDefinitions.find(module => module.id === id).fields
    }
}
