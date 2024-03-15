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


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  standalone: true,
  styleUrls: ['./home.component.scss'],
  imports: [CalendarComponent, HeaderComponent, CommonModule],
  providers:[CalendarService, ImageService]
})
export class HomeComponent {
  
  mealPlanSumResponse: any[] = [];
  datesCreated: string[];
  mealPlansByDay: OrderByDay[] = [];
  start_date: string;
  end_date: string;

  constructor(private http: HttpClient, private authService: AuthService, private imageService: ImageService) {
    this.start_date = "";
    this.end_date = "";
    this.datesCreated = [];
  }

  blurred: boolean = false;
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
  }

  groupmealPlansByDay() {
    this.mealPlansByDay = [];
  
    // Iteration über alle eindeutigen Datumswerte
    this.datesCreated.forEach(date => {
      // Filtern der Mahlzeitenpläne für das aktuelle Datum
      const plansForDay = this.mealPlanSumResponse.filter(plan => plan.mealPlanDate === date);
      
      // Erstellen einer neuen Mahlzeitenplan-Struktur für den aktuellen Tag
      const mealPlansForDay: OrderByDay = { date: date, mealPlans: [], expanded: true };
      mealPlansForDay.mealPlans = plansForDay.map(plan => plan.dishes); // Fügen Sie alle Gerichte für den Tag hinzu
      this.mealPlansByDay.push(mealPlansForDay);
    });
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
          this.mealPlanSumResponse.forEach(meal => {
            if (!this.datesCreated.includes(meal.mealPlanDate)) {
              this.datesCreated.push(meal.mealPlanDate);
            }
          });
          this.groupmealPlansByDay();
        },
        (error) => {
          console.error('Fehler aufgetreten:', error);
          // Fehlermeldung ausgeben
          alert('Fehler aufgetreten: ' + error.message);
          this.mealPlanSumResponse = [];
        }
      );
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
}
