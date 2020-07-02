import {Component, OnInit} from '@angular/core';
import {TestSet} from '../../definitions/TestSet';
import {ActivatedRoute} from '@angular/router';
import {HttpService} from '../../services/http.service';
import {ApiLatestTestsResult} from '../../definitions/api';

@Component({
  selector: 'app-test-builder',
  templateUrl: './start.component.html',
  styleUrls: ['./start.component.scss']
})
export class StartComponent implements OnInit {
  newTest: TestSet = new TestSet();
  presets: any = null;
  lgOpen = false;
  // TODO: Change to false in prod
  metaFormValid = true;
  awaitingResponse = false;
  testResults: ApiLatestTestsResult;
  public error: any;

  constructor(private acr: ActivatedRoute, private http: HttpService) {
    this.acr.data.subscribe(data => {
      this.presets = data.presets;
    });
    this.newTest.settings.hosts.push('172.16.20.90');
    this.newTest.settings.hosts.push('172.16.20.222');
  }

  ngOnInit() {
  }

  launchTest() {
    this.error = null;
    this.testResults = null;
    this.awaitingResponse = true;
    this.http.runTest(this.newTest).subscribe((res: ApiLatestTestsResult) => {
        this.testResults = res;
        this.awaitingResponse = false;
      },
      err => {
        this.error = err;
        this.awaitingResponse = false;
      });
  }
}
