import { DishData } from "./dishData";

export interface Dish extends DishData{
  mealPlanID: number; 
  amount: number;
  expanded: boolean;
}