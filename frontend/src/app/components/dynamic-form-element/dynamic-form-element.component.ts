import {Component, Input, OnInit} from '@angular/core';
import {InputTypes} from "../../definitions/api";

@Component({
    selector: 'app-dynamic-form-element',
    templateUrl: './dynamic-form-element.component.html',
    styleUrls: ['./dynamic-form-element.component.scss']
})
export class DynamicFormElementComponent implements OnInit {

    @Input() inputDefinition: { key: string, value: string };
    @Input() data: any;
    inputTypes = InputTypes;
    newListElem: any = '';
    editableListElem: number = -1;

    constructor() {
    }

    ngOnInit(): void {
    }

    addListElement(key: string) {
        this.data[key] = this.data[key] ? this.data[key] : [];
        if (this.newListElem !== '') {
            this.data[key].push(this.newListElem);
            this.newListElem = '';
        }
    }

    removeListElement(key: string, position: number) {
        this.data[key].splice(position, 1)
    }
}
