import {Component} from '@angular/core';
import {environment} from '../environments/environment';
import {HttpService} from './services/http.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'portal-client';
  themes = [
    'assets/clr-ui.min.css',
    'assets/clr-ui-dark.min.css'
  ];
  linkRef: HTMLLinkElement;
  currTheme = 1;
  serverCheck = 0; // 0: not checked, 1: running, 2: connection problems

  constructor(http: HttpService) {
    this.linkRef = document.getElementById('theme') as HTMLLinkElement;

    http.healthCheck().subscribe(
      () => this.serverCheck = 1,
      () => this.serverCheck = 2);
  }

  switchTheme() {
    this.currTheme = this.currTheme === 1 ? 0 : 1;
    this.linkRef.href = this.themes[this.currTheme];
  }
}
