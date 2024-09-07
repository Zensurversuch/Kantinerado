import {Component, Input, OnInit} from '@angular/core';
import {CommonModule} from "@angular/common";
import {
  FormArray,
  FormBuilder,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import {Suggestion} from '../../interface/suggestion';
import {DishData} from "../../interface/dishData";
import {MealType, MealTypesArray} from "../../interface/mealType";
import {DietaryCategoriesArray, DietaryCategory} from "../../interface/dietaryCategory";
import {HeaderComponent} from "../header/header.component";
import {AllergyService} from "../../service/allergy/allergy.service";
import {FeedbackService} from "../../service/feedback/feedback.service";
import {SuggestionService} from "../../service/suggestion/suggestion.service";

@Component({
  selector: 'app-suggestion-card',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, HeaderComponent],
  templateUrl: './suggestion-card.component.html',
  styleUrls: ['./suggestion-card.scss']
})
export class SuggestionCard implements OnInit {
  @Input() suggestion?: Suggestion;

  dish?: DishData;
  dishForm: FormGroup;
  allergies: string[] = [];
  selectedAllergies: string[] = [];
  dietaryCategories = DietaryCategoriesArray;
  id?:number;

  constructor(private fb: FormBuilder, private allergyService: AllergyService, private feedbackService: FeedbackService, private suggestionService: SuggestionService) {

    this.dishForm = this.fb.group({
      name: ['', Validators.required],
      price: [0, Validators.required],
      ingredients: this.fb.array([this.fb.group({ingredientName: ['']})]),
      dietaryCategory: ['', Validators.required],
      mealType: ['', Validators.required],
      allergies: ['', Validators.required],
      image: ['', Validators.required],
    });
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

    this.dishForm = this.fb.group({
      name: [this.dish?.name, [Validators.required, Validators.maxLength(50)]],
      price: ['', [Validators.required, Validators.maxLength(50), Validators.pattern(/^\d+(\.\d{1,2})?$/)]],
      ingredients: this.fb.array([this.fb.group({ingredientName: ['']})]),
      dietaryCategory: ['', Validators.required],
      mealType: ['', Validators.required],
      allergies: [''],
      image: [this.dish?.image]
    });
    if (this.suggestion) {
      this.id=this.suggestion.dishSuggestion_ID
      console.log(this.id)
      this.dish = {
        name: this.suggestion.name,
        price: 0,
        ingredients: this.suggestion.ingredients || [],
        dietaryCategory: '' as unknown as DietaryCategory,
        mealType: '' as unknown as MealType,
        allergies: [],
        image: this.suggestion.image
      };

      this.dishForm.patchValue({
        name: this.dish?.name,
        price: this.dish?.price,
        dietaryCategory: this.dish?.dietaryCategory,
        mealType: this.dish?.mealType,
        image: this.dish?.image,
        allergies: this.selectedAllergies.join(', ')
      });

      const ingredientsArray = this.dishForm.get('ingredients') as FormArray;
      ingredientsArray.clear();
      this.dish?.ingredients.forEach(ingredient => {
        ingredientsArray.push(this.fb.group({ ingredientName: [ingredient] }));
      });
    }
  }

  get ingredients(): FormArray {
    return this.dishForm.get('ingredients') as FormArray;
  }

  updateAllergies(event: any): void {
    const value = event?.target?.value;
    if (value) {
      const index = this.selectedAllergies.indexOf(value);
      if (index !== -1) {
        this.selectedAllergies.splice(index, 1);
      } else {
        this.selectedAllergies.push(value);
      }
    }
  }

  addIngredient() {
    const ingredientsArray = this.dishForm.get('ingredients') as FormArray;
    ingredientsArray.push(this.fb.group({ ingredientName: [''] }));
  }

  onSubmit() {
    const allIngredients = this.ingredients.value
      .map((ingredient: any) => ingredient.ingredientName)
      .filter((item: string | null) => item !== null)
      .map((item: string) => item.trim());

    const dishData: DishData = {
      name: this.dishForm.value.name,
      price: this.dishForm.value.price,
      ingredients: allIngredients,
      dietaryCategory: this.dishForm.value.dietaryCategory,
      mealType: this.dishForm.value.mealType,
      allergies: this.selectedAllergies,
      image: this.dishForm.get('image')?.value || ''
    };

    this.suggestionService.acceptSuggestion(dishData, this.id).subscribe(
      response => {
        console.log('Dish created successful:', response);
        this.feedbackService.displayMessage(response.response);
      },
      error => {
        console.error('Dish created unsuccessful:', error);
        this.feedbackService.displayMessage(error.error.response);
      }
    );

  }

  onReject() {
    console.log('Suggestion rejected:', this.id); //TODO: löschen

  }

  protected readonly mealTypes = MealTypesArray;

  onImageChange($event: Event) {

  }
}
