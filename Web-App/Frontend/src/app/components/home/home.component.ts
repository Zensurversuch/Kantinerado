import { Component} from '@angular/core';
import { HeaderComponent } from "../header/header.component";
import { CalendarComponent } from "../calendar/calendar.component";
import {CalendarService} from "../../service/calendar/calendar.service";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AllergyService } from '../../service/allergy/allergy.service';
import { AuthService } from '../../service/authentication/auth.service';
import { environment } from '../../../environments/environment';
import {OrderByDay}from '../../interface/order-by-day';
import { CommonModule } from '@angular/common';
import { ImageService } from '../../service/picture/picture.service';
import { FormsModule } from '@angular/forms';
import { Order } from '../../interface/order';
import { MatIconModule } from '@angular/material/icon';
import { Meal } from '../../interface/Meal';
import { trigger, state, style, transition, animate } from '@angular/animations';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectChange, MatSelectModule } from '@angular/material/select';
import { MatTooltipModule } from '@angular/material/tooltip';
import {MatDividerModule} from '@angular/material/divider';
import {MatButtonModule} from '@angular/material/button';
import { FeedbackService } from '../../service/feedback/feedback.service';
import { DishData } from '../../interface/dishData';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  standalone: true,
  styleUrls: ['./home.component.scss'],
  imports: [CalendarComponent, HeaderComponent, CommonModule, FormsModule, MatIconModule, MatFormFieldModule, MatSelectModule, MatTooltipModule,MatDividerModule, MatButtonModule],
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
  start_date: string;
  end_date: string;
  order_list: Order[];
  orderPrice: number;
  quantityOptions: number[] = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
  blurred: boolean = false;
  userAllergies: string[] = [];

  constructor(private http: HttpClient, private authService: AuthService, private feedbackService: FeedbackService, private allergyService: AllergyService) {
    this.start_date = "";
    this.end_date = "";
    this.datesCreated = [];
    this.order_list = [];
    this.ordersByUser = [];
    this.orderPrice= 0;
  }
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
  }
  
  ngOnInit(): void {
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    if(this.isLoggedIn()) {
      const userID = this.authService.getUserID();
      this.allergyService.getAllergiesByUser(userID, headers).subscribe(
        (response: any[]) => {
          this.userAllergies = response.map((allergy: any) => allergy);
          console.log('Allergies:', this.userAllergies);
        },
        error => {
          console.error('Error fetching allergies:', error);
          this.userAllergies = ["Error Loading Allergies"];
        }
      );
    }
  }

  hasMatchingAllergy(dish: any): boolean {
    return dish.dishallergies.some((allergy: string) => this.userAllergies.includes(allergy));
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
  toggleDish(dish: Meal) {
    dish.expanded = !dish.expanded
  }

  getmealPlans() {
    if(this.start_date && this.end_date) {
      const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
  
      this.mealPlanSumResponse = [];
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
          this.feedbackService.displayMessage(error.error.response);
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
      this.feedbackService.displayMessage("Error: Ungültiger Zeitraum: " + changedDate);
    }
  }
  onQuantityChange(event: MatSelectChange, dish: any, mealPlanID: number) {
    const target = event.value;
    if (target !== undefined && target !== null) {
      const quantity = target;
      dish.quantity = quantity;
      const existingOrderIndex = this.order_list.findIndex(order => order.mealPlanID === mealPlanID);
      if (existingOrderIndex !== -1) {
        this.order_list[existingOrderIndex].amount = quantity;
      } else {
        const order = {
          "mealPlanID": mealPlanID,
          "amount": quantity
        };
        this.order_list.push(order);
      }
      this.getOrderPrice();
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
          this.feedbackService.displayMessage("Erfolgreich: Deine Bestellung wurde angelegt");
        },
        (error) => {
          console.error('Fehler aufgetreten:', error.response);
          console.log(error);
          this.feedbackService.displayMessage(error.error.response);
        }
      )
    }
  }
  onPushOrdersButtonClick() {
    if(this.order_list.length !== 0)
    this.pushOrders(this.order_list);
  }
  fillAmountMenus()
  {
    this.ordersByUser.forEach((order: Order) => {
      this.mealPlanSumResponse.forEach(days => {
          days.dishes.forEach((dish: Meal) => {
            if (dish.mealPlanID === order.mealPlanID) {
              dish.amount = order.amount;
            }
        });
      });
    });
    this.getOrderPrice();

  }
  resetAmountMenus()
  {
    if(this.isLoggedIn())
    {
      this.mealPlanSumResponse.forEach(days => {
        days.dishes.forEach((dish: Meal) => {
          dish.amount = 0;
        });
      });
      this.order_list = [];
      this.getOrdersByUser();
    }
  }
  isLoggedIn(): boolean
  {
    return(this.authService.isLoggedIn() && !this.authService.isTokenExpired());
  }
  getOrderPrice()
  { 
    
    const orders: Order[] = [];
    this.orderPrice = 0;

    this.ordersByUser.forEach(order => {
      orders.push({
        amount: order.amount,
        mealPlanID: order.mealPlanID
      });
    });
    this.order_list.forEach(order => {
      const index = orders.findIndex(o => o.mealPlanID === order.mealPlanID)
      if(index !== -1)
      {
        orders[index] = {mealPlanID: order.mealPlanID, amount: order.amount}
      }else{
        orders.push({mealPlanID: order.mealPlanID, amount: order.amount})
      }
    })
    orders.forEach((order: Order) => {
      this.mealPlanSumResponse.forEach(days => {
        days.dishes.forEach((dish: any) => {
          if(order.mealPlanID == dish.mealPlanID)
          {
            this.orderPrice += dish.dishPrice*dish.amount;
          }
        });
      });
      
    });

  }
}
