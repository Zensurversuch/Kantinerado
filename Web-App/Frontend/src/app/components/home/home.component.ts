import { Component } from '@angular/core';
import {HeaderComponent} from "../header/header.component";
import {CalendarComponent} from "../calendar/calendar.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    HeaderComponent,
    CalendarComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
