import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DishData } from '../../interface/dishData';

@Injectable({
  providedIn: 'root'
})
export class DishService {

  constructor(private http: HttpClient) { }

  createDish(dishData: DishData): Observable<any> {
    const url = environment.apiUrl+'/create_dish';
    return this.http.post<any>(url, dishData);
  }
}
