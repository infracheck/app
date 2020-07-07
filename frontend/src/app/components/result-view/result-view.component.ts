import {Component, Input} from '@angular/core';
import {ApiHistory} from '../../definitions/api';

@Component({
    selector: 'app-result-view',
    templateUrl: './result-view.component.html',
    styleUrls: ['./result-view.component.scss']
})
export class ResultViewComponent {
    @Input() HistoryItem: ApiHistory;

    constructor() {
    }

}
