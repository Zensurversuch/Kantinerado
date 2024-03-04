import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { UserData } from '../../interface/user-data';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(private http: HttpClient) { }

  createUser(userData: UserData): Observable<any> {
    const url = '\'http://185.233.106.149:5000/create_user';
    return this.http.post<any>(url, userData);
  }
}
