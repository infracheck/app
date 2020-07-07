import {Component} from '@angular/core';
import {HttpService} from './services/http.service';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.scss']
})
export class AppComponent {
    title = 'portal-client';
    linkRef: HTMLLinkElement;
    serverCheck = 0; // 0: not checked, 1: running, 2: connection problems

    constructor(http: HttpService) {
        this.linkRef = document.getElementById('theme') as HTMLLinkElement;

        http.healthCheck().subscribe(
            () => this.serverCheck = 1,
            () => this.serverCheck = 2);
    }
}
