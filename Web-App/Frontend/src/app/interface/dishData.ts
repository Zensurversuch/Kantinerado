import {DietaryCategory} from "./dietaryCategory";
import {MealType} from "./mealType";

export interface DishData {
  name: string;
  price: number;
  ingredients: [];
  dietaryCategorie: DietaryCategory;
  mealType: MealType;
  allergies: string[];
  image: string;
}
