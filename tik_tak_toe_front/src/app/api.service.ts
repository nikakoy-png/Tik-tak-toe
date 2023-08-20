import { Injectable } from '@angular/core';
import {HttpClient} from "@angular/common/http";
import {Observable} from "rxjs";
import {RegistrationDto} from "./models/registration.dto";
import {environment} from "./environments/environment";
import {LoginDto} from "./models/login.dto";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) { }

  register(userData: RegistrationDto): Observable<any> {
    return this.http.post(`${environment.apiUrl}api/register/`, userData);
  }

  login(userData: LoginDto): Observable<any> {
    console.log('take')
    console.log(userData)
    return this.http.post(`${environment.apiUrl}api/login/`, userData);
  }
}
