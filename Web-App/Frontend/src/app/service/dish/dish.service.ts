import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../../environments/environment';
import { DishData } from '../../interface/dishData';
import { AuthService } from '../authentication/auth.service';
import {MealType} from "../../interface/mealType";

@Injectable({
  providedIn: 'root'
})
export class DishService {

  constructor(private http: HttpClient, private authService: AuthService) { }

  createDish(dishData: DishData): Observable<any> {
    const url = environment.apiUrl+'/create_dish';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.post<any>(url, dishData, { headers });
  }

  getDishByMealType(mealType: string){
    const url = environment.apiUrl+'/dish_by_mealType/'+mealType.toString();
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.get<any>(url,{ headers });
  }
}
