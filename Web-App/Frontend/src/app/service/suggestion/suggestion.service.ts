import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../authentication/auth.service";
import {SuggestionData} from "../../interface/suggestion-data";
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";
import {Suggestion} from "../../interface/suggestion";
import {DishData} from "../../interface/dishData";

@Injectable({
  providedIn: 'root'
})
export class SuggestionService {
  constructor(private http: HttpClient, private authService: AuthService) {
  }

  createSuggestion(suggestion: SuggestionData): Observable<any> {
    const url = environment.apiUrl + '/create_dish_suggestion';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.post<any>(url, suggestion, {headers});
  }

  getAllSuggestions(): Observable<Suggestion[]> {
    const url = environment.apiUrl + '/all_dish_suggestions';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.get<any>(url, {headers});
  }

  deleteSuggestion(id?: number): Observable<any> {
    const url = environment.apiUrl + '/delete_dish_suggestion';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.get(url + `/${id}`, {headers});
  }


  acceptSuggestion(suggestionData: DishData, id?: number): Observable<any> {
    const url = environment.apiUrl + '/accept_dish_suggestion';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    const payload = {
      dishSuggestionID: id,
      dishData: {
        name: suggestionData.name,
        price: suggestionData.price,
        ingredients: suggestionData.ingredients,
        dietaryCategory: suggestionData.dietaryCategory,
        mealType: suggestionData.mealType,
        image: "test",
        allergies: suggestionData.allergies
      }
    };
    return this.http.post(url, payload, {headers});
  }
}
