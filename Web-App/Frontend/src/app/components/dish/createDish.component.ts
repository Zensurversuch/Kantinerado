import {Component, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormControl, FormGroup, FormsModule, isFormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {NgIf} from "@angular/common";
import {UserData} from '../../interface/user-data';
import {UserService} from '../../service/user/user.service';
import {HttpClientModule} from "@angular/common/http";
import {Role} from "../../interface/role";
import { CommonModule } from '@angular/common';
import { DietaryCategories, DietaryCategoriesArray } from '../../interface/dietaryCategories';
import { MealTypesArray } from '../../interface/mealTypes';


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

  constructor(private fb: FormBuilder) {}

  ngOnInit(): void {
    this.createDishForm = this.fb.group({
      name: ['', Validators.required],
      ingredients: this.fb.array([]), // Initialize with empty array
      dietaryCategory: ['', Validators.required],
      mealType: ['', Validators.required]
    });
  }

  get ingredients(): FormArray {
    return this.createDishForm.get('ingredients') as FormArray;
  }

  createIngredientFormGroup(): FormGroup {
    return this.fb.group({
      ingredientName: [''] // Set the default value to an empty string
    });
  }

  addIngredient(): void {
    this.ingredients.push(this.createIngredientFormGroup());
  }

  getControls() {
    return (this.createDishForm.get('ingredients') as FormArray).controls;
  }

  registerUser(): void {
    const dishData = this.createDishForm.value;
    console.log('Name:', dishData.name);
    
    const allIngredients = this.ingredients.value.map((ingredient: any) => ingredient.ingredientName);
    console.log('Ingredients:', allIngredients);

    console.log('Dietary Category:', dishData.dietaryCategory);
    console.log('Meal Type:', dishData.mealType);

    // Your form submission logic goes here
  }
}