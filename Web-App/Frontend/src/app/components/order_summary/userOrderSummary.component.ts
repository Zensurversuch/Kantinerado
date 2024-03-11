import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../../service/authentication/auth.service';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../header/header.component';
import { CalendarComponent } from '../calendar/calendar.component';
import { CalendarService } from '../../service/calendar/calendar.service';

interface OrderByDay {
  date: string;
  orders: any[];
  expanded?: boolean;
}

@Component({
  selector: 'app-userOrderSummary',
  standalone: true,
  imports: [
    FormsModule,
    HeaderComponent,
    CommonModule,
    CalendarComponent
  ],
  providers:[CalendarService],
  styleUrls: ['./userOrderSummary.component.scss'],
  templateUrl: './userOrderSummary.component.html'
})
export class UserOrderSummaryComponent {
  orderSumResponse: any[] = [];
  datesCreated: string[];
  ordersByDay: OrderByDay[] = [];
  start_date: string | null;
  end_date: string | null;
  calendarComponent: CalendarComponent;

  constructor(private http: HttpClient, private authService: AuthService, private calendarService: CalendarService) {
    this.start_date = "2024-01-01";
    this.end_date = "2024-12-01";
    this.datesCreated = [];
    this.calendarComponent = new CalendarComponent(this.calendarService);
    this.getOrders();
  }

  groupOrdersByDay() {
    for (const date of this.datesCreated) {
      const groupedOrdersForDay = [];
      for (const order of this.orderSumResponse) {
        if (order.mealPlanDate === date) {
            groupedOrdersForDay.push(order);
        }
      }
      this.ordersByDay.push({ date: date, orders: groupedOrdersForDay, expanded:true });
    }
  }
  

  formatDate(dateString: string): string {
    const options: Intl.DateTimeFormatOptions = { weekday: 'long', year: 'numeric', month: '2-digit', day: '2-digit' };
    const date = new Date(dateString);
    const formattedDate = date.toLocaleDateString('de-DE', options);
    const parts = formattedDate.split(', ');
    return `${parts[0]}, ${parts[1]}`;
  }

  toggleDay(day: OrderByDay) {
    day.expanded = !day.expanded;
  }

  getOrders() {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);

    this.http.get<any[]>(`${environment.apiUrl}/orders_by_user/${this.start_date}/${this.end_date}`, { headers })
    .subscribe(
      (orderSumResponse) => {
        console.log('GET-Anfrage erfolgreich', orderSumResponse);
        this.orderSumResponse = orderSumResponse;
        this.orderSumResponse.forEach(order => {
          if (!this.datesCreated.includes(order.mealPlanDate)) {
            this.datesCreated.push(order.mealPlanDate);
          }
        });
        this.groupOrdersByDay();
      },
      (error) => {
        console.error('Fehler aufgetreten:', error);
        this.orderSumResponse = [];
      }
    );
  }

  setDates() {
    this.start_date = this.calendarComponent.getFormattedStart();
    this.end_date = this.calendarComponent.getFormattedEnd();

    console.log("START: " + this.start_date);
    console.log("ENDE: " + this.end_date);

    this.getOrders();
  }

}
