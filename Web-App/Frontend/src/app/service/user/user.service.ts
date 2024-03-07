import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserData } from '../../interface/user-data';
import { environment } from '../../../environments/environment';
import { AuthService } from '../authentication/auth.service';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient, private authService: AuthService) { }

  createUser(userData: UserData): Observable<any> {
    const url = environment.apiUrl+'/create_user';
    return this.http.post<any>(url, userData);
  }

  createAdmin(userData: UserData): Observable<any> {
    const url = environment.apiUrl+'/create_user_as_admin';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.post<any>(url, userData, { headers });
  }
}
