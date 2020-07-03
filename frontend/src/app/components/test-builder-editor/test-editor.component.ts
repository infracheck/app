import {Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {Test} from '../../definitions/TestSet';
import {ApiPlugin} from '../../definitions/api';


@Component({
  selector: 'app-test-editor',
  templateUrl: './test-editor.component.html',
  styleUrls: ['./test-editor.component.scss']
})
export class TestEditorComponent implements OnInit {
  testSet: Test[] = [];

  @Output() testSetChange = new EventEmitter();

  @Input() get test() {
    return this.testSet;
  }

  set test(set) {
    this.testSet = set;
    this.testSetChange.emit(this.testSet);
  }

  public apiTestResults: ApiPlugin[];
  public settingsContent: { testData: Test, apiTestResult: ApiPlugin };
  activeSettings = -1;
  searchTerm = '';


  constructor(private acr: ActivatedRoute) {
    this.acr.data.subscribe(data => {
      this.apiTestResults = data.tests;
    });
  }

  ngOnInit() {
  }


  toggleSettings(test: Test) {
    this.settingsContent = {
      testData: test,
      apiTestResult: this.apiTestResults.find(apiTest => apiTest.id === test.id)
    };
  }

  removeTest(i: number) {
    this.test.splice(i, 1);
  }

  addTest(test: any) {
    this.test.push(new Test(test));
  }
}
