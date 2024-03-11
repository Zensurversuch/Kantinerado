import { Component } from '@angular/core';
import {MatDatepickerModule} from "@angular/material/datepicker";
import {DateRange } from '@angular/material/datepicker';
import {MatFormFieldModule} from "@angular/material/form-field";
import {JsonPipe} from "@angular/common";
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {provideNativeDateAdapter} from "@angular/material/core";

@Component({
  selector: 'app-calendar',
  standalone: true,
  imports: [MatFormFieldModule, MatDatepickerModule, FormsModule, ReactiveFormsModule, JsonPipe],
  providers: [provideNativeDateAdapter()],
  templateUrl: './calendar.component.html',
  styleUrl: './calendar.component.scss'
})
export class CalendarComponent {
  selectedRange: DateRange<Date> | undefined;

  constructor() {
    // Initialisieren Sie die ausgewählte Range hier, wenn benötigt
  }
  range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null),
  });
}
