import {Injectable} from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../authentication/auth.service";

@Injectable({
  providedIn: 'root'
})
export class MealPlanService {


  constructor(private http: HttpClient, private authService: AuthService) {
  }


  createMealPlan(MealPlan: { mealPlan: { "dishID": number; "date": string; }[] }) {
    const url = environment.apiUrl + '/create_meal_plan';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    this.http.post<any>(url, MealPlan, {headers})
      .subscribe({
        next: value => console.log(value.message),
        error: err => console.error(err.message),
        complete: () => console.log('Observable emitted the complete notification')
      });
  }
}
