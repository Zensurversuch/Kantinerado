import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthService} from "../authentication/auth.service";
import {suggestionData} from "../../interface/suggestion-data";
import {Observable} from "rxjs";
import {environment} from "../../../environments/environment";

@Injectable({
  providedIn: 'root'
})
export class SuggestionService {

  constructor(private http: HttpClient, private authService: AuthService) { }

  createSuggestion(suggestedDish: suggestionData): Observable<any> {
    const url = environment.apiUrl+'/create_dish_suggestion';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.post<any>(url, suggestedDish, { headers });
  }

  getAllSuggestions(): Observable<any[]> {
    const url = environment.apiUrl+'/all_dish_suggestions';
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    return this.http.get<any>(url, {headers});
  }

  deleteSuggestion(id: number): Observable<any> {
    const url = environment.apiUrl+'/delete_dish_suggestion';
    return this.http.delete(url+`/${id}`);
  }

  // Methode zum Akzeptieren und Erweitern eines Vorschlags
  acceptSuggestion(suggestionData: any): Observable<any> {
    const url = environment.apiUrl+'/delete_dish_suggestion';
    return this.http.post(url, suggestionData);
  }
}
