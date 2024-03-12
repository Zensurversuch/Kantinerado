import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {AuthService} from '../../service/authentication/auth.service';
import {FormsModule} from '@angular/forms';
import {HeaderComponent} from '../header/header.component';
import {CalendarService} from "../../service/calendar/calendar.service";
import {CalendarComponent} from "../calendar/calendar.component";

interface OrderByDay {
  date: string;
  dishes: any[];
  expanded?: boolean;
}

@Component({
  selector: 'app-workerOrderSummary',
  standalone: true,
  imports: [
    FormsModule,
    HeaderComponent,
    CommonModule,
    CalendarComponent
  ],
  providers: [CalendarService],
  styleUrls: ['./workerOrderSummary.component.scss'],
  templateUrl: './workerOrderSummary.component.html'
})
export class WorkerOrderSummaryComponent {
  orderSumResponse: any[] = [];
  start_date: string;
  end_date: string;
  ordersByDay: OrderByDay[] = []

  constructor(private http: HttpClient, private authService: AuthService,) {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    this.start_date = 'placeholder'     // MUSS WENN KALENDER IMPLEMENTIERT IST ÜBER KALENDER GESETZT WERDEN
    this.end_date = 'placeholder'       // MUSS WENN KALENDER IMPLEMENTIERT IST ÜBER KALENDER GESETZT WERDEN

    this.http.get<any[]>(`${environment.apiUrl}/orders_sorted_by_dish/${this.start_date}/${this.end_date}`, {headers})
      .subscribe(
        (orderSumResponse) => {
          console.log('GET request successful', orderSumResponse);
          this.orderSumResponse = orderSumResponse;

          this.ordersByDay = this.orderSumResponse.map(order => ({
            date: order.mealPlanDate,
            dishes: order.dishes,
            expanded: true
          }));
        },
        (error) => {
          console.error('Error occurred:', error);
          this.orderSumResponse = [];
        }
      );
  }

  formatDate(dateString: string): string {
    const options: Intl.DateTimeFormatOptions = {weekday: 'long', year: 'numeric', month: '2-digit', day: '2-digit'};
    const date = new Date(dateString);
    const formattedDate = date.toLocaleDateString('de-DE', options);
    const parts = formattedDate.split(', ');
    return `${parts[0]}, ${parts[1]}`;
  }

  toggleDay(orders: OrderByDay) {
    orders.expanded = !orders.expanded;
  }

  changedEndDateHandler(EndDate: string) {
    if (EndDate != undefined)
      this.end_date = EndDate;
  }

  changedStartDateHandler(StartDate: string) {
    if (StartDate != undefined)
      this.start_date = StartDate;
  }
}
