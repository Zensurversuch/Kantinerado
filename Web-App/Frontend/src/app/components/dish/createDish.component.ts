import {Component, OnInit} from '@angular/core';
import {FormArray, FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {NgIf} from "@angular/common";
import {DishService} from '../../service/dish/dish.service';
import {HttpClientModule} from "@angular/common/http";
import { CommonModule } from '@angular/common';
import { DietaryCategoriesArray } from '../../interface/dietaryCategory';
import { MealTypesArray } from '../../interface/mealType';
import { AllergyService } from '../../service/allergy/allergy.service';
import { DishData } from '../../interface/dishData';
import { FeedbackService } from '../../service/feedback/feedback.service';



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

  constructor(private fb: FormBuilder, private allergyService: AllergyService, private dishService: DishService, private feedbackService: FeedbackService ) {}

  blurred: boolean = false;
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
  }

  ngOnInit(): void {
    this.allergyService.getAllergies().subscribe(
      response => {
        this.allergies = response.map((allergy: any) => allergy.name);
      },
      error => {
        this.feedbackService.displayMessage(error.error.response);
        this.allergies = ["Error Loading Allergies"];
      }
    );

    this.createDishForm = this.fb.group({
      name: ['', [Validators.required, Validators.maxLength(50)]],
      price: ['', [Validators.required,Validators.maxLength(50), Validators.pattern(/^\d+(\.\d{1,2})?$/)]],
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
      if (file.type !== 'image/png') {
        event.target.value = ''; 
        this.createDishForm.patchValue({ image: '' });
        this.feedbackService.displayMessage("Warnung: Bitte wähle ein PNG als Bild");
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        event.target.value = ''; 
        this.createDishForm.patchValue({ image: '' }); 
        this.feedbackService.displayMessage("Warnung: Das Bild ist größer als die maximale Größe von 10MB");

      } else {
        const reader = new FileReader();
        reader.onload = () => {
          let base64String = reader.result as string;
          base64String = base64String.replace(/^data:image\/[a-z]+;base64,/, '');
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
    price:  this.createDishForm.value.price,
    ingredients: allIngredients,
    dietaryCategory: this.createDishForm.value.dietaryCategory,
    mealType: this.createDishForm.value.mealType,
    allergies: this.selectedAllergies,
    image: this.createDishForm.get('image')?.value || ''
  };

  console.log('Dish Form Data:', dishData);

  this.dishService.createDish(dishData).subscribe(
    response => {
      console.log('Dish created successful:', response);
      this.createDishForm.reset();
      this.feedbackService.displayMessage(response.response);

    },
    error => {
      console.error('Dish created unsuccessful:', error);
      this.feedbackService.displayMessage(error.error.response);
    }
  );

  }
}