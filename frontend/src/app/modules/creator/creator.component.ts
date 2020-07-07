import {Component, OnInit} from '@angular/core';
import {ApiPlugin} from "../../definitions/api";
import {ActivatedRoute} from "@angular/router";

@Component({
    selector: 'app-test-creator',
    templateUrl: './creator.component.html',
    styleUrls: ['./creator.component.scss']
})
export class CreatorComponent implements OnInit {
    open_wizard: boolean = true;

    public plugins: ApiPlugin[];


    constructor(private acr: ActivatedRoute) {
        this.acr.data.subscribe(data => {
            this.plugins = data.tests;
        });

    }

    ngOnInit(): void {
    }

}
