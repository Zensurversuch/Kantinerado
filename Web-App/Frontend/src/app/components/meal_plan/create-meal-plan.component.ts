import {Component, OnInit} from '@angular/core';
import {CdkDrag, CdkDragDrop, CdkDropList, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';
import {CalendarService} from "../../service/calendar/calendar.service";
import {MealTypesArray} from "../../interface/mealType";
import {FormControl, FormGroup, FormsModule, ReactiveFormsModule} from "@angular/forms";
import {DishService} from "../../service/dish/dish.service";
import {MatOption} from "@angular/material/autocomplete";
import {MatFormField, MatLabel, MatSelect} from "@angular/material/select";
import {MatCard} from "@angular/material/card";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {HeaderComponent} from "../header/header.component";
import {WeekdayArray} from "../../interface/weekday";
import {MatButton} from "@angular/material/button";
import {Dish} from "../../interface/dish";
import {MealPlanService} from "../../service/mealPlan/meal-plan.service";
import { FeedbackService } from '../../service/feedback/feedback.service';


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
    MatButton,
    ReactiveFormsModule,
    NgIf,
    NgClass,
  ],
  templateUrl: './create-meal-plan.component.html',
  styleUrl: './create-meal-plan.component.scss',
})
export class CreateMealPlanComponent implements OnInit {
  public MealPlanForm: FormGroup;

  constructor(protected calendarService: CalendarService, private dishService: DishService, private mealPlanService: MealPlanService) {
    this.MealPlanForm = new FormGroup({
      Monday: new FormControl(this.mondayList),
      Tuesday: new FormControl(this.tuesdayList),
      Wednesday: new FormControl(this.wednesdayList),
      Thursday: new FormControl(this.thursdayList),
      Friday: new FormControl(this.fridayList),
      Saturday: new FormControl(this.saturdayList)
    });
  }

  ngOnInit(): void {
    this.dates = this.calendarService.getWeekDatesInTwoWeeks()
  }


  dates: string[] = [];
  weekday: string[] = WeekdayArray;
  mealTypes: string[] = MealTypesArray;
  dishesAfterType: Dish[] = [];
  selectedDish: Dish | undefined;
  selectedMealType: string | undefined;
  dishList: Dish [] = [];
  mondayList: Dish [] = [];
  tuesdayList: Dish [] = [];
  wednesdayList: Dish [] = [];
  thursdayList: Dish [] = [];
  fridayList: Dish [] = [];
  saturdayList: Dish [] = [];

  [key: string]: any;

  createDishPlan() {
    const mealPlanArray: { mealPlan: { "dishID": number; "date": string; }[] } = {mealPlan: []};
    const weekDayLists = ['mondayList', 'tuesdayList', 'wednesdayList', 'thursdayList', 'fridayList', 'saturdayList'];
    weekDayLists.forEach((dayList, index) => {
      this[dayList].forEach((dish: Dish) => {
        const dishJSON = {"dishID": dish.dish_id, "date": this.dates[index]};
        mealPlanArray.mealPlan.push(dishJSON)
      })
    })
    this.mealPlanService.createMealPlan(mealPlanArray)
  }

  loadDishes() {
    this.dishesAfterTypex = [];
    if (this.selectedMealType) {
      this.dishService.getDishByMealType(this.selectedMealType)
        .subscribe((data: Dish[]) => {
          this.dishesAfterType = data;
          //Fehlermeldung
        });
    }
  }

  drop(event: CdkDragDrop<Dish[]>) {
    if (event.previousContainer === event.container) {
      moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
    } else {
      transferArrayItem(event.previousContainer.data, event.container.data, event.previousIndex, event.currentIndex)
    }
    this.checkLists();
    console.log(event)
  }

  createNewDishCard() {
    if (this.selectedDish) {
      this.dishList.push(this.selectedDish);
      this.selectedDish = undefined;
    }
  }

  checkLists(): void {
    const weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    let allHaveDish = true;
    let allVegetarian = false;

    weekdays.forEach(day => {
      const control = this.MealPlanForm.get(day);

      if (control && control.value) {
        if (!(control.value.length > 0)) {
          allHaveDish = false;
          control.setErrors({'noDish': true});
        } else if (control.value.some((dish: Dish) => dish.dietaryCategorie.toString() === 'Vegetarisch')) {
          control.setErrors(null);
          allVegetarian = true;
        } else {
          control.setErrors({'noVegetarianDish': true});
        }
      }
    });

    const control = this.MealPlanForm.get("Saturday");
    let saturdaySoup = false;
    if (control?.value.some((dish: Dish) => dish.mealType.toString() === 'Suppe')) {
      saturdaySoup = true;
      control?.setErrors({'soupOnSaturday': true});
    } else if(control?.getError('saturdaySoup')){
      control?.setErrors(null);
    }

    if (allHaveDish && allVegetarian && !saturdaySoup) {
      this.MealPlanForm.setErrors(null);
    } else {
      this.MealPlanForm.setErrors({'missingDish': true});
    }
  }
}
