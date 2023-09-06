import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {Observable} from "rxjs";
import {RegistrationDto} from "./models/registration.dto";
import {environment} from "./environments/environment";
import {LoginDto} from "./models/login.dto";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) {
  }

  register(userData: RegistrationDto): Observable<any> {
    return this.http.post(`${environment.apiUrl}api/register/`, userData);
  }

  login(userData: LoginDto): Observable<any> {
    return this.http.post(`${environment.apiUrl}api/login/`, userData);
  }

  getUserById(userId: number): Observable<any> {
    return this.http.get(`${environment.apiUrl}api/get_user/${userId}/`);
  }

  getUsersOrderByRating(): Observable<any> {
    return this.http.get(`${environment.apiUrl}api/get_user_order_by_rating/`)
  }

  getUserByToken(jwtToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiUrl}api/login/`, { headers });
  }
}
