import { Component } from '@angular/core';
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatFormFieldModule} from "@angular/material/form-field";
import {JsonPipe} from "@angular/common";
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {provideNativeDateAdapter} from "@angular/material/core";
import {CalendarService} from "../../service/calendar/calendar.service";

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [MatFormFieldModule, MatDatepickerModule, FormsModule, ReactiveFormsModule, JsonPipe],
  providers: [provideNativeDateAdapter()],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.scss'
})
export class CalendarComponent {

  range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null),
  });
  formattedStart: string | null = null;
  formattedEnd: string | null = null;

  constructor(
    private calendarService: CalendarService
  ) {
    this.range = this.calendarService.getDefaultRangeFormGroup();


    this.range.get('start')?.valueChanges.subscribe((newValue: Date | null) => {
      if (newValue) {
        this.formattedStart = calendarService.convertToDate(newValue);
        console.log(this.formattedStart)
      } else {
        this.formattedStart = null;
      }
    });

    this.range.get('end')?.valueChanges.subscribe((newValue: Date | null) => {
      if (newValue) {
        this.formattedEnd = calendarService.convertToDate(newValue);
        console.log(this.formattedEnd)
      } else {
        this.formattedEnd = null;
      }
    });
    console.log(this.formattedStart)
    console.log(this.formattedEnd)
  }
  setCurrentWeek() {
    this.calendarService.setCurrentWeek(this.range);
  }

  setNextWeek() {
    this.calendarService.setNextWeek(this.range);
  }
}
