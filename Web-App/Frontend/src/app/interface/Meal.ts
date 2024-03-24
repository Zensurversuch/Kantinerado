import { DishData } from "./dishData";

export interface Meal extends DishData{
  mealPlanID: number; 
  amount: number;
  expanded: boolean;
}