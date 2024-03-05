import {Component, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormControl, FormGroup, FormsModule, isFormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {NgIf} from "@angular/common";
import {DishService} from '../../service/dish/dish.service';
import {HttpClientModule} from "@angular/common/http";
import { CommonModule } from '@angular/common';
import { DietaryCategoriesArray } from '../../interface/dietaryCategory';
import { MealTypesArray } from '../../interface/mealType';
import { AllergyService } from '../../service/allergy/allergy.service';
import { DishData } from '../../interface/dishData';


@Component({
  selector: 'app-createDish',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    FormsModule,
    HeaderComponent,
    NgIf,
    HttpClientModule,
    CommonModule
  ],
  templateUrl: './createDish.component.html',
  styleUrl: './createDish.component.scss'
})
export class CreateDishComponent implements OnInit {
  createDishForm!: FormGroup;
  dietaryCategories = DietaryCategoriesArray;
  mealTypes = MealTypesArray;
  allergies: string[] = [];
  selectedAllergies: string[] = [];

  constructor(private fb: FormBuilder, private allergyService: AllergyService, private dishService: DishService) {}

  ngOnInit(): void {
    this.allergyService.getAllergies().subscribe(
      response => {
        this.allergies = response.map((allergy: any) => allergy.name);
      },
      error => {
        console.error('Error fetching allergies:', error);
        this.allergies = ["Error Loading Allergies"];
      }
    );

    this.createDishForm = this.fb.group({
      name: ['', Validators.required],
      ingredients: this.fb.array([]),
      dietaryCategory: ['', Validators.required],
      mealType: ['', Validators.required],
      allergies: [''],
      image: ['']
    });
  }

  get ingredients(): FormArray {
    return this.createDishForm.get('ingredients') as FormArray;
  }

  onImageChange(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      if (file.size > 10 * 1024 * 1024) {
        event.target.value = ''; // Clear the input value to reset it
        this.createDishForm.patchValue({ image: '' }); // Reset the image FormControl value
        alert('File size exceeds the limit of 10MB.'); // Display an error message to the user
      } else {
        const reader = new FileReader();
        reader.onload = () => {
          const base64String = reader.result as string;
          this.createDishForm.patchValue({ image: base64String });
        };
        reader.readAsDataURL(file);
      }
    }
  }

  addIngredient(): void {
    this.ingredients.push(this.createIngredientFormGroup());
  }

  createIngredientFormGroup(): FormGroup {
    return this.fb.group({
      ingredientName: ['']
    });
  }

  updateAllergies(event: any): void {
    const value = event?.target?.value;
    if (value) {
      const index = this.selectedAllergies.indexOf(value);
      if (index !== -1) {
        this.selectedAllergies.splice(index, 1); // Remove the allergy if unchecked
      } else {
        this.selectedAllergies.push(value); // Add the allergy if checked
      }
    }
  }

  createDishSubmit(): void {
  const allIngredients = this.ingredients.value
    .map((ingredient: any) => ingredient.ingredientName)
    .filter((item: string) => item.trim() !== "");

  const dishData: DishData = {
    name: this.createDishForm.value.name,
    ingredients: allIngredients,
    dietaryCategory: this.createDishForm.value.dietaryCategory,
    mealType: this.createDishForm.value.mealType,
    allergies: this.selectedAllergies.map((allergyName: string) => ({ name: allergyName })),
    image: this.createDishForm.get('image')?.value || ''
  };

  console.log('Dish Form Data:', dishData);



  this.dishService.createDish(dishData).subscribe(
    response => {
      console.log('Dish created successful:', response);
    },
    error => {
      console.error('Dish created unsuccessful:', error);

    }
  );

  }
}