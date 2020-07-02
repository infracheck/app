import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ApiTestsResult} from '../../definitions/api';

@Component({
  selector: 'app-documentation',
  templateUrl: './documentation.component.html',
  styleUrls: ['./documentation.component.scss']
})
export class DocumentationComponent implements OnInit {

  public tests: ApiTestsResult[];

  selectedTestId;
  testDirs: string[];

  constructor(private acr: ActivatedRoute) {
    this.acr.data.subscribe(data => {
      this.tests = data.tests;
      this.testDirs = Array.from(new Set(this.tests.map(test => test.directory)));
    });

  }

  ngOnInit() {
    this.selectedTestId = this.tests[0].id;
  }

  selectTestId(testDesc: string) {
    this.selectedTestId = testDesc;
  }

  getTestsOfCategory(category: string): ApiTestsResult[] {
    return this.tests.filter(test => test.directory === category);
  }
}
