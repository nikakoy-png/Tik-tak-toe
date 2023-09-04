import {Injectable} from '@angular/core';
import {HttpClient, HttpParams} from "@angular/common/http";
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

  getTimer(hashCodePlay: string, player_id: number): Observable<any> {
    const params = new HttpParams().set('play_hash_code', hashCodePlay).set('player_id', player_id)
    return this.http.get(`${environment.apiUrl}api/get_timer_turn/`, {params});
  }

  getUserById(userId: number): Observable<any> {
    return this.http.get(`${environment.apiUrl}api/get_user/${userId}/`);
  }

  getUserByToken(): Observable<any> {
    return this.http.get(`${environment.apiUrl}api/login/`);
  }
}
