import {Injectable} from '@angular/core';
import {Observable, throwError} from 'rxjs';
import {environment} from '../../environments/environment';
import {HttpClient, HttpErrorResponse, HttpHeaders} from '@angular/common/http';
import {catchError} from 'rxjs/operators';
import {ApiLatestTestsResult, ApiPlugin} from '../definitions/api';
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


    getLatestTests(): Observable<ApiLatestTestsResult[]> {
        return this.http.get<ApiLatestTestsResult[]>(`${url}/latest_tests`).pipe(
            catchError(HttpService.handleError)
        );
    }

    getTestResult(resultId: string): Observable<ApiLatestTestsResult> {
        return this.http.get<ApiLatestTestsResult>(`${url}/latest_tests/${resultId}`).pipe(
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
