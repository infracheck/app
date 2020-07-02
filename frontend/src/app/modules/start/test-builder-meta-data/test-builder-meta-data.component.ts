import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {TestSet} from '../../../definitions/TestSet';
import {FormControl, FormGroup} from '@angular/forms';

@Component({
  selector: 'app-test-builder-meta-data',
  templateUrl: './test-builder-meta-data.component.html',
  styleUrls: ['./test-builder-meta-data.component.scss']
})
export class TestBuilderMetaDataComponent implements OnInit {

  @Input() testSet: TestSet;
  @Output() formValid = new EventEmitter<boolean>();

  newHost: string;
  metaForm = new FormGroup({
    description: new FormControl('Description'),
    name: new FormControl('test test'),
    platform: new FormControl('linux'),
    username: new FormControl('root'),
    password: new FormControl('start#123')
  });

  constructor() {
  }

  ngOnInit() {
    this.isFormValid();
  }

  addHost() {
    this.testSet.settings.hosts.push(this.newHost);
    this.newHost = '';
    this.isFormValid();
  }

  removeHost(host: string) {
    this.testSet.settings.hosts = this.testSet.settings.hosts.filter(entry => entry !== host);
    this.isFormValid();
  }

  isFormValid() {
    if (this.metaForm.valid && this.testSet.settings.hosts.length > 0) {
      const form = this.metaForm.value;
      this.testSet.settings = {
        hosts: this.testSet.settings.hosts,
        user: form.username,
        target_os: form.platform,
        password: form.password,
        name: form.name,
        description: form.description
      };
      this.formValid.emit(true);
    } else {
      this.formValid.emit(false);
    }
  }

}
