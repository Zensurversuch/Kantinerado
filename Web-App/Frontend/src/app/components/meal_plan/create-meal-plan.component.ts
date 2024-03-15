import {Component, NgIterable, Type} from '@angular/core';
import {MatOption} from "@angular/material/autocomplete";
import {MatFormField, MatLabel, MatSelect} from "@angular/material/select";
import {MatCard} from "@angular/material/card";
import {CdkDragDrop, CdkDropList} from "@angular/cdk/drag-drop";
import {NgForOf, NgIf} from "@angular/common";
import {HeaderComponent} from "../header/header.component";
import {CalendarService} from "../../service/calendar/calendar.service";
import {MealTypesArray} from "../../interface/mealType";
import {DishData} from "../../interface/dishData";
import {FormsModule} from "@angular/forms";
import {DishService} from "../../service/dish/dish.service";

@Component({
  selector: 'app-create-meal-plan',
  standalone: true,
  imports: [
    MatOption,
    MatSelect,
    MatLabel,
    MatCard,
    MatFormField,
    CdkDropList,
    NgForOf,
    HeaderComponent,
    NgIf,
    FormsModule
  ],
  templateUrl: './create-meal-plan.component.html',
  styleUrl: './create-meal-plan.component.scss'
})
export class CreateMealPlanComponent{
  constructor(private calendarService: CalendarService, private dishService: DishService) {

  }


  weekDates= this.calendarService.getWeekDatesInTwoWeeks()
  mealTypes: string[] = MealTypesArray;
  dishes: (NgIterable<DishData>) | undefined;
  selectedDish: any;
  selectedMealType: any;

  onDrop($event: CdkDragDrop<any, any>) {


  }

  loadDishes() {
    if (this.selectedMealType) {
      this.dishService.getDishByMealType(this.selectedMealType)
        .subscribe((data: NgIterable<DishData> | undefined) => {
          this.dishes = data;
        });
    }
  }
}

