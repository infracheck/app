import {Component, Input, OnInit} from '@angular/core';
import {ApiPlugin} from "../../../definitions/api";
import {FormGroup} from "@angular/forms";

@Component({
    selector: 'app-plugin-data-input',
    templateUrl: './plugin-data-input.component.html',
    styleUrls: ['./plugin-data-input.component.scss']
})
export class PluginDataInputComponent implements OnInit {

    @Input() pluginDocumentation: ApiPlugin;
    @Input() pluginData;

    ngOnInit() {
    }


    constructor() {
    }


    onSubmit() {

    }
}
