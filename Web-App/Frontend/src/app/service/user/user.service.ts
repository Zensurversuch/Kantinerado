import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserData } from '../../interface/user-data';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) { }

  createUser(userData: UserData): Observable<any> {
    const url = environment.apiUrl+'/create_user';
    return this.http.post<any>(url, userData);
  }
}
