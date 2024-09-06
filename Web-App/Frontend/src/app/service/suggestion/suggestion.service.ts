import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../authentication/auth.service";
import {SuggestedDish} from "../../interface/suggested-dish";
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class SuggestionService {

  constructor(private http: HttpClient, private authService: AuthService) { }

  createSuggestion(suggestedDish: SuggestedDish): Observable<any> {
    const url = environment.apiUrl+'/create_dish_suggestion';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.post<any>(url, suggestedDish, { headers });
  }
}
