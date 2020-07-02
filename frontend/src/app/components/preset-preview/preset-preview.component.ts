import {Component, Input, OnInit} from '@angular/core';
import {Preset} from '../../definitions/Preset';
import {HttpService} from '../../services/http.service';
import {ApiTestsResult} from '../../definitions/api';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-preset-preview',
  templateUrl: './preset-preview.component.html',
  styleUrls: ['./preset-preview.component.scss']
})
export class PresetPreviewComponent implements OnInit {

  @Input() preset: Preset;
  @Input() edit: boolean;
  public apiTestResults: ApiTestsResult[];

  constructor(private http: HttpService, private acr: ActivatedRoute) {
    this.acr.data.subscribe(data => {
      this.apiTestResults = data.tests;
    });
  }

  ngOnInit() {
  }
}
