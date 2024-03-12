import { Component} from '@angular/core';
import { HeaderComponent } from "../header/header.component";
import { CalendarComponent } from "../calendar/calendar.component";
import {CalendarService} from "../../service/calendar/calendar.service";

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  standalone: true,
  styleUrls: ['./home.component.scss'],
  imports: [CalendarComponent, HeaderComponent],
  providers:[CalendarService]
})
export class HomeComponent {
  calendarComponent :CalendarComponent = new CalendarComponent(this.calendarService);

  constructor(private calendarService: CalendarService) {

  }
  start_date: string | undefined;
  end_date: string | undefined ;


  changedStartDateHandler(StartDate: string) {
    if (StartDate != undefined)
      this.start_date = StartDate;
    console.log("Startdatum:"+this.start_date)
  }
  changedEndDateHandler(EndDate: string) {
    if (EndDate != undefined)
      this.end_date = EndDate;
    console.log("EndDatum:"+this.end_date)
  }
}
