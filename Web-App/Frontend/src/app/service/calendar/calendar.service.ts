import { Injectable } from '@angular/core';
import {formatDate} from "@angular/common";
import {FormControl, FormGroup, Validators} from "@angular/forms";
import {environment} from "../../../environments/environment";
import {HttpClient} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class CalendarService {

  constructor(private http: HttpClient) { }
  convertToDate(stringToFormat: Date) {
    return formatDate(stringToFormat, 'yyyy-MM-dd', 'en-US', 'GMT+1');
  }

  setCurrentWeek(range: FormGroup): void {
    const url = environment.apiUrl+'/get_this_week';
    this.http.get<any>(url).subscribe(data => {
      range.get('start')?.setValue(new Date(data.monday));
      range.get('end')?.setValue(new Date(data.sunday));
    });
  }

  setNextWeek(range: FormGroup): void {
    const url = environment.apiUrl+'/get_next_week';
    this.http.get<any>(url).subscribe(data => {
      range.get('start')?.setValue(new Date(data.monday));
      range.get('end')?.setValue(new Date(data.sunday));
    });
  }
}
