import {Component, Input, OnInit} from '@angular/core';
import {ApiInputPluginData, ApiPlugin} from "../../../definitions/api";

@Component({
    selector: 'app-plugin-data-input',
    templateUrl: './plugin-data-input.component.html',
    styleUrls: ['./plugin-data-input.component.scss']
})
export class PluginDataInputComponent implements OnInit {

    @Input() pluginDocumentation: ApiPlugin;
    @Input() pluginData: ApiInputPluginData;

    ngOnInit() {
    }


    constructor() {
    }


    onSubmit() {

    }
}
