import {Injectable} from '@angular/core';
import {Observable, throwError} from 'rxjs';
import {environment} from '../../environments/environment';
import {HttpClient, HttpErrorResponse, HttpHeaders, HttpParams} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {ApiHistory, ApiPlugin} from '../definitions/api';
import {TestSet} from '../definitions/TestSet';
import {Preset} from '../definitions/Preset';


export const url = environment.server;

@Injectable({
    providedIn: 'root'
})
export class HttpService {

    constructor(private http: HttpClient) {
    }

    private static handleError(error: HttpErrorResponse) {
        if (error.error instanceof ErrorEvent) {
            console.error('An error occurred:', error.error.message);
        } else {
            console.error(
                `Backend returned code ${error.status}, ` +
                `body was: ${error.error}`);
        }
        return throwError(
            `Something bad happened; please try again later. ${error.error}`);
    }

    getPlugins(): Observable<ApiPlugin[]> {
        return this.http.get<ApiPlugin[]>(`${url}/plugins`).pipe(
            catchError(HttpService.handleError)
        );
    }

    runTest(testSet: TestSet): Observable<any> {
        const httpOptions = {
            headers: new HttpHeaders({
                'Content-Type': 'application/json'
            })
        };

        return this.http.post(`${url}/run`, testSet, httpOptions).pipe(
            catchError(HttpService.handleError)
        );
    }


    getHistory(limit: number = 100, offset: number = 0): Observable<ApiHistory[]> {
        let params = new HttpParams();

        params = params.append('limit', limit.toString());
        params = params.append('offset', offset.toString());
        return this.http.get<ApiHistory[]>(`${url}/history`, {
            params: params
        }).pipe(
            catchError(HttpService.handleError)
        );
    }


    healthCheck() {
        return this.http.get<any>(`${url}/check`).pipe(
            catchError(HttpService.handleError)
        );
    }


    getAllPresets(): Observable<Preset[]> {
        return this.http.get<Preset[]>(`${url}/presets`).pipe(
            catchError(HttpService.handleError)
        );
    }

}
