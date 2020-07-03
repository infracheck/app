import {Component, OnInit} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {ApiModule, ApiPlugin} from '../../definitions/api';

@Component({
  selector: 'app-documentation',
  templateUrl: './documentation.component.html',
  styleUrls: ['./documentation.component.scss']
})
export class DocumentationComponent implements OnInit {

  public plugins: ApiPlugin[];

  selectedModule: ApiModule;

  constructor(private acr: ActivatedRoute) {
    this.acr.data.subscribe(data => {
      this.plugins = data.tests;
    });

  }

  ngOnInit() {
    this.selectedModule = this.plugins[0].modules[0];
  }
}
