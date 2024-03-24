import { Component} from '@angular/core';
import { HeaderComponent } from "../header/header.component";
import { CalendarComponent } from "../calendar/calendar.component";
import {CalendarService} from "../../service/calendar/calendar.service";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../../service/authentication/auth.service';
import { environment } from '../../../environments/environment';
import {OrderByDay}from '../../interface/order-by-day';
import { CommonModule } from '@angular/common';
import { ImageService } from '../../service/picture/picture.service';
import { FormsModule } from '@angular/forms';
import { Order } from '../../interface/order';
import { MatIconModule } from '@angular/material/icon';
import { Dish } from '../../interface/dish';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  standalone: true,
  styleUrls: ['./home.component.scss'],
  imports: [CalendarComponent, HeaderComponent, CommonModule, FormsModule, MatIconModule, MatFormFieldModule, MatSelectModule],
  providers:[CalendarService, ImageService],
  animations: [
    trigger('expandCollapse', [
      state('collapsed', style({ height: '0', overflow: 'hidden' })),
      state('expanded', style({ height: '*', overflow: 'hidden' })),
      transition('collapsed => expanded', animate('0.3s ease-in')),
      transition('expanded => collapsed', animate('0.3s ease-out'))
    ])
  ]
})
export class HomeComponent {
  
  mealPlanSumResponse: any[] = [];
  ordersByUser: Array<Order>;
  datesCreated: string[];
  mealPlansByDay: OrderByDay[] = [];
  start_date: string;
  end_date: string;
  order_list: Order[];
  quantityOptions: number[] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

  constructor(private http: HttpClient, private authService: AuthService) {
    this.start_date = "";
    this.end_date = "";
    this.datesCreated = [];
    this.order_list = [];
    this.ordersByUser = [];
  }
    blurred: boolean = false;
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
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
  toggleDish(dish: Dish) {
    dish.expanded = !dish.expanded
  }

  getmealPlans() {
    if(this.start_date && this.end_date) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
  
      this.mealPlanSumResponse = [];
      this.mealPlansByDay = [];
      this.datesCreated = [];
  
      this.http.get<any[]>(`${environment.apiUrl}/meal_plan/${this.start_date}/${this.end_date}`, { headers })
      .subscribe(
        (mealPlanSumResponse) => {
          console.log('meal_plan/'+this.start_date+'/'+this.end_date + ' GET-Anfrage erfolgreich', mealPlanSumResponse);
          this.mealPlanSumResponse = mealPlanSumResponse;
          //resets chosen orders if new date is chosen
          this.order_list = [];
          this.resetAmountMenus();
          
        },
        (error) => {
          console.error('Fehler aufgetreten:', error);
          this.mealPlanSumResponse = [];
        }
      );
    }
  }
  getOrdersByUser(){
    if(this.start_date && this.end_date) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
      this.http.get<any[]>(`${environment.apiUrl}/orders_by_user/${this.start_date}/${this.end_date}`, { headers })
      .subscribe(
        (ordersByUserResponse) => {
          console.log('orders_by_user/'+this.start_date+'/'+this.end_date + ' GET-Anfrage erfolgreich', ordersByUserResponse);
          this.ordersByUser = ordersByUserResponse;
          this.fillAmountMenus();
        },
        (error) => {
          console.error('Fehler aufgetreten:', error);
          this.ordersByUser = [];
        }
      )
    }
  }

  changedDateHandler(changedDate: string[] | undefined) {
    if (changedDate && changedDate.length === 2 && changedDate.every(date => !!date)) {
      this.start_date = changedDate[0];
      this.end_date = changedDate[1];
      console.log("Handler Start: " + this.start_date);
      console.log("Handler End: " + this.end_date);
      
      this.getmealPlans();
      
      
    } else {
      console.error("Invalid date range:", changedDate);
    }
  }
  onQuantityChange(event: MatSelectChange, dish: any, mealPlanID: any) {
    const target = event.value as HTMLSelectElement;
    if (target) {
      const quantity = target.value;
      dish.quantity = quantity;
      const existingOrderIndex = this.order_list.findIndex(order => order.mealPlanID === mealPlanID);
    if (existingOrderIndex !== -1) {
      this.order_list[existingOrderIndex].amount = quantity;
    } else {
      const order = {
        mealPlanID: mealPlanID,
        amount: quantity
      };
      this.order_list.push(order);
    }
    }
  }
  pushOrders(orders: Array<Object>)
  {
    if(orders && this.isLoggedIn()) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
      headers.set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
      this.http.post(environment.apiUrl+'/create_order', {"orders": orders}, { headers })
      .subscribe(
        (response: any) => {
          console.log('POST request successful', response);
        },
        (error) => {
          console.error('Fehler aufgetreten:', error.response);
          console.log(error);
          alert('Fehler aufgetreten: ' + error.message);
        }
      )
    }
  }
  onPushOrdersButtonClick() {
    this.pushOrders(this.order_list);
  }
  fillAmountMenus()
  {
    this.ordersByUser.forEach((order: Order) => {
      this.mealPlanSumResponse.forEach(days => {
          days.dishes.forEach((dish: Dish) => {
            if (dish.mealPlanID === order.mealPlanID) {
              dish.amount = order.amount;
            }
        });
      });
    });

  }
  resetAmountMenus()
  {
    if(this.isLoggedIn())
    {
      this.mealPlanSumResponse.forEach(days => {
        days.dishes.forEach((dish: Dish) => {
          dish.amount = 0;
        });
      });
      this.getOrdersByUser();
    }
  }
  isLoggedIn(): boolean
  {
    return(this.authService.isLoggedIn() && !this.authService.isTokenExpired());
  }
}
