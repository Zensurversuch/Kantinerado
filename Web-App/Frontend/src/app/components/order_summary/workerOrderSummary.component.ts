import {Component} from '@angular/core';
import {CommonModule} from '@angular/common';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {AuthService} from '../../service/authentication/auth.service';
import {FormsModule} from '@angular/forms';
import {HeaderComponent} from '../header/header.component';
import {CalendarService} from "../../service/calendar/calendar.service";
import {CalendarComponent} from "../calendar/calendar.component";
import jspdf from 'jspdf';
import html2canvas from 'html2canvas';

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
  styleUrls: ['./summary.component.scss'],
  templateUrl: './workerOrderSummary.component.html'
})
export class WorkerOrderSummaryComponent {
  orderSumResponse: any[] = [];
  start_date: string;
  end_date: string;
  ordersByDay: OrderByDay[] = []

  constructor(private http: HttpClient, private authService: AuthService,) {
    this.start_date = "";
    this.end_date = "";
  }

  blurred: boolean = false;
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
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

  getOrders() {
    if(this.start_date && this.end_date) {

      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);

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
        app-header, .calendar-container, #drucken_btn {
          display: none !important;
        }
      }
    `;
    document.head.appendChild(style);
  
    window.print();
  
    document.head.removeChild(style);
  }
  
  
  
}
  

