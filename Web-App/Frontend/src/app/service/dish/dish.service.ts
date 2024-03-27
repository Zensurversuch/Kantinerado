import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DishData } from '../../interface/dishData';
import { AuthService } from '../authentication/auth.service';
import { FeedbackService } from '../../service/feedback/feedback.service';
import { tap } from 'rxjs/operators';


@Injectable({
  providedIn: 'root'
})
export class DishService {

  constructor(private http: HttpClient, private authService: AuthService,  private feedbackService: FeedbackService) { }

  createDish(dishData: DishData): Observable<any> {
    const url = environment.apiUrl+'/create_dish';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.post<any>(url, dishData, { headers });
  }

  getDishByMealType(mealType: string): Observable<any> {
    const url = environment.apiUrl+'/dish_by_mealType/'+mealType.toString();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.get<any>(url,{ headers }).pipe(
      tap(
        value => console.log(value.message),
        error => {
          console.error(error.message);
          this.feedbackService.displayMessage(error.error.response);
        }
      )
    );
  }
}
