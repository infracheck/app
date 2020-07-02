import {Component, Input, OnInit} from '@angular/core';
import {ApiLatestTestsResult} from '../../definitions/api';

@Component({
  selector: 'app-result-view',
  templateUrl: './result-view.component.html',
  styleUrls: ['./result-view.component.scss']
})
export class ResultViewComponent implements OnInit {
  @Input() results: ApiLatestTestsResult;

  constructor() {
  }

  ngOnInit() {
  }


}
