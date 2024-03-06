import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class AllergyService {

  constructor(private http: HttpClient) { }

  getAllergies(): Observable<any> {
    const url = environment.apiUrl+'/all_allergies';
    return this.http.get<any>(url);
  }
}
