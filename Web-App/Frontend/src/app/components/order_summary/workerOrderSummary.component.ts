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
    this.expandAllDays(); // Expand all days
    await new Promise(resolve => setTimeout(resolve, 1000)); // Wait for the expansion to complete
  
    const data = document.getElementById('printSummary');
    if (data) {
      const A4_HEIGHT = 841.89;
      const A4_WIDTH = 595.28;
  
      const WIDTH_MARGIN = 10;
      const HEIGHT_MARGIN = 10;
      const PAGE_HEIGHT = A4_HEIGHT - 2 * HEIGHT_MARGIN;
  
      const pdf = new jspdf('p', 'pt', 'a4');
      const canvas = await html2canvas(data as HTMLElement);
  
      const canvasWidth = canvas.width;
      const canvasHeight = canvas.height;
  
      const imgWidth = A4_WIDTH - 2 * WIDTH_MARGIN;
      const imgHeight = (imgWidth / canvasWidth) * canvasHeight;
  
      const pageImg = canvas.toDataURL('image/png', 1.0);
  
      let position = HEIGHT_MARGIN;
      if (imgHeight > PAGE_HEIGHT) { // need multi-page pdf
        let heightUnprinted = imgHeight;
        while (heightUnprinted > 0) {
          pdf.addImage(
            pageImg,
            'PNG',
            WIDTH_MARGIN,
            position,
            imgWidth,
            Math.min(imgHeight, PAGE_HEIGHT) // Use the smaller of imgHeight and PAGE_HEIGHT
          );
  
          // Draw the margin top and margin bottom if needed
          pdf.setFillColor(255, 255, 255);
          pdf.rect(0, 0, A4_WIDTH, HEIGHT_MARGIN, 'F'); // margin top
          pdf.rect(0, A4_HEIGHT - HEIGHT_MARGIN, A4_WIDTH, HEIGHT_MARGIN, 'F'); // margin bottom
  
          heightUnprinted -= PAGE_HEIGHT;
          position += PAGE_HEIGHT; // next vertical placement
  
          // Add another page if there's more contents to print
          if (heightUnprinted > 0) pdf.addPage();
        }
      } else {
        // Print single-page pdf
        pdf.addImage(
          pageImg,
          'PNG',
          WIDTH_MARGIN,
          HEIGHT_MARGIN,
          imgWidth,
          imgHeight
        );
      }
  
      // Save the pdf
      pdf.save(`myPDF.pdf`);
    }
  }
}
  

