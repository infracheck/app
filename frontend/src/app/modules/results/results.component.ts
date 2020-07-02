import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {HttpService} from '../../services/http.service';
import {ApiLatestTestsResult} from '../../definitions/api';

@Component({
  selector: 'app-results',
  templateUrl: './results.component.html',
  styleUrls: ['./results.component.scss']
})
export class ResultsComponent implements OnInit {
  selectedResult: ApiLatestTestsResult;
  resultId = '';
  fetchError = false;
  latestTests: ApiLatestTestsResult[];

  constructor(private acr: ActivatedRoute, private http: HttpService) {
    this.resultId = this.acr.snapshot.paramMap.get('id');
    if (this.resultId) {
      this.fetchResult();
    }

    this.acr.data.subscribe(data => {
      this.latestTests = data.latest;
    });
  }

  ngOnInit() {
  }

  fetchResult() {
    this.http.getTestResult(this.resultId).subscribe(
      (res) => {
        this.selectedResult = res;
      }
    );
  }
}
