import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../../service/authentication/auth.service';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../header/header.component';
import { CalendarService } from '../../service/calendar/calendar.service';
import { CalendarComponent } from '../calendar/calendar.component';

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
  styleUrls: ['./summary.component.scss'],
  templateUrl: './userOrderSummary.component.html'
})
export class UserOrderSummaryComponent {
  orderSumResponse: any[] = [];
  datesCreated: string[];
  ordersByDay: OrderByDay[] = [];
  start_date: string;
  end_date: string;

  constructor(private http: HttpClient, private authService: AuthService) {
    this.start_date = "";
    this.end_date = "";
    this.datesCreated = [];
  }

  blurred: boolean = false;


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
    if(this.start_date && this.end_date) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
  
      this.orderSumResponse = [];
      this.ordersByDay = [];
      this.datesCreated = [];
  
      this.http.get<any[]>(`${environment.apiUrl}/orders_by_user/${this.start_date}/${this.end_date}`, { headers })
      .subscribe(
        (orderSumResponse) => {
          console.log('orders_by_user/'+this.start_date+'/'+this.end_date + ' GET-Anfrage erfolgreich', orderSumResponse);
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
  }

  changedDateHandler(changedDate: string[] | undefined) {
    if (changedDate != undefined) {
      this.start_date = changedDate[0];
      this.end_date = changedDate[1];
      console.log("Handler Start: " + this.start_date);
      console.log("Handler End: " + this.end_date);

      this.getOrders();
    }
  }

  ToggleBlurred(isOpened: boolean) {
      this.blurred = isOpened;
  }

  expandAllDays(): void {
    this.ordersByDay.forEach(day => {
      day.expanded = true; // Assuming 'expanded' is the property indicating if a day is expanded
    });
  }

  async generatePDF(): Promise<void> {
    this.expandAllDays();

    await new Promise(resolve => setTimeout(resolve, 1000));
  
    const style = document.createElement('style');
    style.innerHTML = `
      @media print {
        app-header, .calendar-container, .print-button {
          display: none !important;
        }
      }
    `;
    document.head.appendChild(style);
  
    window.print();
    document.head.removeChild(style);
  }
}
