import {Component, EventEmitter, Output} from '@angular/core';
import {MatDatepickerModule} from "@angular/material/datepicker";
import {MatFormFieldModule} from "@angular/material/form-field";
import {JsonPipe} from "@angular/common";
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MAT_DATE_LOCALE, provideNativeDateAdapter} from "@angular/material/core";
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

  @Output() changedDate = new EventEmitter<string[]|undefined>();


  range = new FormGroup({
    start: new FormControl<Date | null>(null),
    end: new FormControl<Date | null>(null),
  });
  formattedStart: string | undefined
  formattedEnd: string | undefined

  oldDateStart: string | undefined;
  oldDateEnd: string | undefined;


  constructor(
    private calendarService: CalendarService
  ) {
    this.calendarService.setCurrentWeek(this.range);

    this.range.get('start')?.valueChanges.subscribe((newValue: Date | null) => {
      if (newValue) {
        this.formattedStart = calendarService.convertToDate(newValue);
      }
    });

    this.range.get('end')?.valueChanges.subscribe((newValue: Date | null) => {
      if (newValue) {
        this.formattedEnd = calendarService.convertToDate(newValue);
        this.emitChangedEvent()
      }
    });
  }

  setCurrentWeek() {
    this.calendarService.setCurrentWeek(this.range);
  }

  setNextWeek() {
    this.calendarService.setNextWeek(this.range);
  }

  emitChangedEvent() {
    if (this.formattedEnd != undefined && this.formattedStart != undefined) {
      if (this.oldDateEnd != this.formattedEnd || this.oldDateStart != this.formattedStart) {
        const dateArray:string[]|undefined  = []
        dateArray?.push(this.formattedStart)
        dateArray?.push(this.formattedEnd)
        this.changedDate.emit(dateArray)
        this.oldDateEnd=this.formattedEnd;
        this.oldDateStart=this.formattedStart
      }
    }
  }

}
