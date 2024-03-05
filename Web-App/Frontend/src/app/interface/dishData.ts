import { Allergy } from "./allergy";
import { DietaryCategory } from "./dietaryCategory";
import { MealType } from "./mealType";

export interface DishData {
    name: string;
    ingredients: [];
    dietaryCategory: DietaryCategory;
    mealType: MealType;
    allergies: Allergy[];
    image: string;
  }
  