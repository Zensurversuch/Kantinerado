import {Component} from '@angular/core';
import {CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';
import {CalendarService} from "../../service/calendar/calendar.service";
import {MealTypesArray} from "../../interface/mealType";
import {DishData} from "../../interface/dishData";
import {FormsModule} from "@angular/forms";
import {DishService} from "../../service/dish/dish.service";
import {MatOption} from "@angular/material/autocomplete";
import {MatFormField, MatLabel, MatSelect} from "@angular/material/select";
import {MatCard} from "@angular/material/card";
import {NgForOf} from "@angular/common";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-create-meal-plan',
  standalone: true,
  imports: [
    FormsModule,
    MatOption,
    MatSelect,
    MatLabel,
    MatFormField,
    MatCard,
    NgForOf,
    CdkDrag,
    HeaderComponent,
    CdkDropList,
  ],
  templateUrl: './create-meal-plan.component.html',
  styleUrl: './create-meal-plan.component.scss'
})
export class CreateMealPlanComponent {
  constructor(protected calendarService: CalendarService, private dishService: DishService) {
  }

  mealTypes: string[] = MealTypesArray;
  dishesAfterType: DishData[] = [];
  selectedDish: DishData | undefined;
  selectedMealType: string | undefined;
  dishList :DishData []= [];
  mondayList:DishData []= [];
  tuesdayList:DishData []= [];
  wednesdayList:DishData []= [];
  thursdayList:DishData []= [];
  fridayList:DishData []= [];
  saturdayList:DishData []= [];



  loadDishes() {
    if (this.selectedMealType) {
      this.dishService.getDishByMealType(this.selectedMealType)
        .subscribe((data: DishData[]) => {
          this.dishesAfterType = data;
        });
    }
  }

  drop(event: CdkDragDrop<DishData[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data, event.container.data, event.previousIndex, event.currentIndex )
    }
    console.log(event)
  }

  createNewDishCard() {
    if (this.selectedDish) {
      this.dishList.push(this.selectedDish);
      this.selectedDish = undefined;
    }
  }
}
