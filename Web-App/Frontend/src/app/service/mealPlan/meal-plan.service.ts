import {Injectable} from '@angular/core';
import {environment} from "../../../environments/environment";
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../authentication/auth.service";
import {Observable} from "rxjs";
import { FeedbackService } from '../../service/feedback/feedback.service';


@Injectable({
  providedIn: 'root'
})
export class MealPlanService {


  constructor(private http: HttpClient, private authService: AuthService, private feedbackService: FeedbackService) {
  }


  createMealPlan(MealPlan: { mealPlan: { "dishID": number; "date": string; }[] }) {
    const url = environment.apiUrl + '/create_meal_plan';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    this.http.post<any>(url, MealPlan, {headers})
      .subscribe({
        next: value => console.log(value.message),
        error: error => {
          console.error(error.message);
          this.feedbackService.displayMessage(error.error.response);
        },
        complete: () => this.feedbackService.displayMessage("Erfolgreich: Der Speiseplan wurde angelegt"),

      });
  }
  

  getMealPlans(start_date: string, end_date:string): Observable<any> {
    const url = environment.apiUrl+'/meal_plan/'+start_date+'/'+end_date;
    return this.http.get<any>(url);
  }
}
