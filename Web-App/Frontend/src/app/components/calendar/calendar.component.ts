import {Component, EventEmitter, Output} from '@angular/core';
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

  @Output() changedStartDate = new EventEmitter<string>();
  @Output() changedEndDate = new EventEmitter<string>();

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
    this.range = this.calendarService.getDefaultRangeFormGroup();

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
    if (this.formattedEnd != undefined &&
      this.formattedStart != undefined) {
      if (this.oldDateEnd != this.formattedEnd) {
        this.changedEndDate.emit(this.formattedEnd);
        this.oldDateEnd = this.formattedEnd;
      }
      if (this.oldDateStart != this.formattedStart) {
        this.changedStartDate.emit(this.formattedStart);
        this.oldDateStart = this.formattedStart;
      }
    }
  }
}
