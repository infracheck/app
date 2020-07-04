import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {HttpService} from '../../services/http.service';
import {ApiHistory} from '../../definitions/api';
import {ClrDatagridSortOrder} from "@clr/angular";

@Component({
    selector: 'app-results',
    templateUrl: './results.component.html',
    styleUrls: ['./results.component.scss']
})
export class ResultsComponent {
    selected: ApiHistory;
    history: ApiHistory[];
    resultId: string;
    sort_desc = ClrDatagridSortOrder.DESC;

    constructor(private acr: ActivatedRoute, private http: HttpService) {
        this.resultId = this.acr.snapshot.paramMap.get('id');
        if (this.resultId) {
            console.log("IMPLEMENT THIS FEATURE");
        }

        this.acr.data.subscribe(data => {
            this.history = data.latest;
        });
    }
}
