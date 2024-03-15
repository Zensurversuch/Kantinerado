import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class mealPlanService {

  constructor(private http: HttpClient) { }

  getMealPlans(start_date: string, end_date:string): Observable<any> {
    const url = environment.apiUrl+'/meal_plan/'+start_date+'/'+end_date;
    return this.http.get<any>(url);
  }
}