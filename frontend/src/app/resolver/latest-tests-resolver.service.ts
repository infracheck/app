import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs';
import {HttpService} from '../services/http.service';
import {ApiHistory} from '../definitions/api';

@Injectable({
    providedIn: 'root'
})
export class LatestTestsResolverService implements Resolve<ApiHistory[]> {

    constructor(private http: HttpService) {
    }

    resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<ApiHistory[]> {
        return this.http.getHistory();
    }
}
