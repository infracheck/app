import {Injectable} from '@angular/core';
import {ActivatedRouteSnapshot, Resolve, RouterStateSnapshot} from '@angular/router';
import {Observable} from 'rxjs';
import {HttpService} from '../services/http.service';
import {Preset} from '../definitions/Preset';

@Injectable({
  providedIn: 'root'
})
export class PresetResolverService implements Resolve<Preset[]> {

  constructor(private http: HttpService) {
  }

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<Preset[]> {
    return this.http.getAllPresets();
  }
}
