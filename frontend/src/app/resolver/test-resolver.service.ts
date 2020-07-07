import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs';
import {HttpService} from '../services/http.service';
import {ApiPlugin} from '../definitions/api';

@Injectable({
    providedIn: 'root'
})
export class PluginResolver implements Resolve<any> {

    constructor(private http: HttpService) {
    }

    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<ApiPlugin[]> {
        return this.http.getPlugins();
    }
}
