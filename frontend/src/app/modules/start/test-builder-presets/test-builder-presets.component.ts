import {Component, Input, OnInit} from '@angular/core';
import {Test, TestSet} from '../../../definitions/TestSet';
import {ApiPlugin} from '../../../definitions/api';
import {ActivatedRoute} from '@angular/router';
import {Preset} from '../../../definitions/Preset';

@Component({
  selector: 'app-test-builder-presets',
  templateUrl: './test-builder-presets.component.html',
  styleUrls: ['./test-builder-presets.component.scss']
})
export class TestBuilderPresetsComponent implements OnInit {

  @Input() presets: Preset[];
  @Input() testSet: TestSet;
  testsWithoutPresets: Test[];


  selected: Preset[] = [];
  public settingsContent: { testData: Test, apiTestResult: ApiPlugin };
  activeSettings = -1;
  public apiTestResults: ApiPlugin[];


  constructor(private acr: ActivatedRoute) {
    this.acr.data.subscribe(data => {
      this.apiTestResults = data.tests;
    });
  }

  ngOnInit() {
    this.testsWithoutPresets = this.testSet.testset;
  }

  toggleSettings(test: Test) {
    this.settingsContent = {
      testData: test,
      apiTestResult: this.apiTestResults.find(apiTest => apiTest.id === test.id)
    };
  }

  onSelectionChange() {
    this.testSet.testset = this.testsWithoutPresets;
    this.selected.forEach((selectedTest: Preset) => {
      this.testSet.testset = this.testSet.testset.concat(selectedTest.testset);
    });
  }
}
