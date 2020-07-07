import {Component, Input, OnInit} from '@angular/core';
import {FormGroup} from "@angular/forms";

@Component({
    selector: 'app-dynamic-form-element',
    templateUrl: './dynamic-form-element.component.html',
    styleUrls: ['./dynamic-form-element.component.scss']
})
export class DynamicFormElementComponent implements OnInit {

    @Input() input: { key: string, value: string };

    constructor() {
    }

    ngOnInit(): void {
    }

}
