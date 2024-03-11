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
  getDefaultMonday(): Date {
    const today = new Date();
    const currentDayOfWeek = today.getDay(); // 0 for Sunday, 1 for Monday, ..., 6 for Saturday

    // Berechne die Differenz in Tagen, um zum aktuellen Montag zu gelangen
    const daysUntilMonday = currentDayOfWeek === 0 ? 6 : currentDayOfWeek - 1;
    const currentMonday = new Date(today);
    currentMonday.setDate(today.getDate() - daysUntilMonday);
    return currentMonday;
  }

  getDefaultSaturday(): Date {
    const currentMonday = this.getDefaultMonday();

    // Füge 5 Tage hinzu, um zu Samstag zu gelangen
    const currentSaturday = new Date(currentMonday);
    currentSaturday.setDate(currentMonday.getDate() + 5);
    return currentSaturday;
  }

  getDefaultRangeFormGroup(): FormGroup {
    return new FormGroup({
      start: new FormControl<Date>(this.getDefaultMonday(), Validators.required),
      end: new FormControl<Date>(this.getDefaultSaturday(), Validators.required),
    });
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
