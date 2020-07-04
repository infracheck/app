import {Component, Input, OnInit} from '@angular/core';
import {Test} from '../../definitions/TestSet';
import {ApiPlugin} from '../../definitions/api';

@Component({
  selector: 'app-test-settings-modal',
  templateUrl: './test-settings-modal.component.html',
  styleUrls: ['./test-settings-modal.component.scss']
})
export class TestSettingsModalComponent implements OnInit {
  @Input() test: Test;
  @Input() apiTestResult: ApiPlugin;
  public inputData: { field: string, type: string }[] = [];
  newListElem = '';

  constructor() {
  }

  ngOnInit() {

    Object.keys(this.apiTestResult.modules).forEach(key => {
      this.inputData.push({
        field: key,
        type: this.apiTestResult.id[key]
      });
    });
  }

  removeListElem(list: any[], elem: any) {
    return list.filter(element => elem !== element);
  }

  addListElem(list: any[]) {
    list = list ? list : [];
    list.push(this.newListElem);
    this.newListElem = '';
    return list;
  }
}
