import { ChangeDetectorRef, Component, NgIterable } from '@angular/core';
import {CdkDrag, CdkDragDrop, CdkDropList} from '@angular/cdk/drag-drop';
import { CalendarService } from "../../service/calendar/calendar.service";
import { MealTypesArray } from "../../interface/mealType";
import { DishData } from "../../interface/dishData";
import { FormsModule } from "@angular/forms";
import { DishService } from "../../service/dish/dish.service";
import { MatOption } from "@angular/material/autocomplete";
import { MatFormField, MatLabel, MatSelect } from "@angular/material/select";
import { MatCard } from "@angular/material/card";
import { NgForOf } from "@angular/common";
import { HeaderComponent } from "../header/header.component";

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
  constructor(private calendarService: CalendarService, private dishService: DishService, private cdr: ChangeDetectorRef) { }

  weekDates = this.calendarService.getWeekDatesInTwoWeeks();
  mealTypes: string[] = MealTypesArray;
  dishes: (NgIterable<DishData>) | undefined;
  selectedDish: any;
  selectedMealType: any;
  dragItems: { [key: string]: DishData[] } = {};

  ngOnInit() {
    this.weekDates.forEach(day => {
      this.dragItems[day] = [];
    });
  }

  onDrop(event: CdkDragDrop<DishData[]>, day: string) {
    if (event.previousContainer === event.container) {
      // Verschiebe das Element innerhalb der Liste, wenn es in derselben Liste bleibt
      const draggedItem = this.dragItems[day][event.previousIndex];
      this.dragItems[day] = [...this.dragItems[day].slice(0, event.previousIndex), draggedItem, ...this.dragItems[day].slice(event.previousIndex + 1)];
    } else {
      // Verschiebe das Element von einer Liste in eine andere
      const droppedItem = event.previousContainer.data[event.previousIndex];
      this.dragItems[day].push(droppedItem);
      event.previousContainer.data.splice(event.previousIndex, 1);
    }
  }

  loadDishes() {
    if (this.selectedMealType) {
      this.dishService.getDishByMealType(this.selectedMealType)
        .subscribe((data: NgIterable<DishData> | undefined) => {
          this.dishes = data;
        });
    }
  }

  createNewDragItem() {
    if (this.selectedDish) {
      // Füge das ausgewählte Gericht für jeden Tag der Woche hinzu
      this.weekDates.forEach(day => {
        this.dragItems[day].push(this.selectedDish);
      });
      this.cdr.detectChanges();
    }
  }
}
