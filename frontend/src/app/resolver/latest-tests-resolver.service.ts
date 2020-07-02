import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs';
import {HttpService} from '../services/http.service';
import {ApiLatestTestsResult} from '../definitions/api';

@Injectable({
  providedIn: 'root'
})
export class LatestTestsResolverService implements Resolve<ApiLatestTestsResult[]> {

  constructor(private http: HttpService) {
  }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<ApiLatestTestsResult[]> {
    return this.http.getLatestTests();
  }
}
