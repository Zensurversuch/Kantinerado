import { Component } from '@angular/core';
import {MatCalendar, MatDatepicker, MatDatepickerInput, MatDatepickerToggle} from "@angular/material/datepicker";
import {MatFormField} from "@angular/material/form-field";
import {DatePipe} from "@angular/common";

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [
    MatDatepickerInput,
    MatFormField,
    MatDatepickerToggle,
    MatDatepicker,
    MatCalendar,
    DatePipe
  ],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.scss'
})
export class CalendarComponent {
  currentDate: Date | null = new Date();
}
