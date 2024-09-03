import {Component, OnInit} from '@angular/core';
import {HeaderComponent} from "../header/header.component";
import {FeedbackService} from "../../service/feedback/feedback.service";
import {suggestionData} from "../../interface/suggestion-data"
import {SuggestionService} from "../../service/suggestion/suggestion.service";
import {NgClass, NgForOf, NgIf} from "@angular/common";
import {
  FormArray,
  FormBuilder,
  FormControl,
  FormGroup,
  FormsModule,
  ReactiveFormsModule,
  Validators
} from "@angular/forms";
import {HttpClient} from "@angular/common/http";

@Component({
  selector: 'app-dish_suggestion',
  standalone: true,
  imports: [
    HeaderComponent,
    NgClass,
    FormsModule,
    NgIf,
    ReactiveFormsModule,
    NgForOf
  ],
  templateUrl: './dishSuggestion.html',
  styleUrl: '../suggestion.component.scss'
})
export class DishSuggestionComponent implements OnInit{
  blurred: boolean = false;
  createDishSuggestionForm!: FormGroup;

  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
  }

  ngOnInit(): void {
    this.createDishSuggestionForm = this.fb.group({
      title: new FormControl("", [Validators.required, Validators.maxLength(50)]),
      description: new FormControl("", [Validators.maxLength(150)]),
      ingredients: this.fb.array([this.fb.group({ingredientName: ['']})]),
      image: new FormControl("", [])
    });
  }


  constructor(private fb: FormBuilder, private http: HttpClient, private feedbackService: FeedbackService, private suggestionService: SuggestionService) {
  }


  addIngredient(): void {
    this.ingredients.push(this.createIngredientFormGroup());
  }

  createIngredientFormGroup(): FormGroup {
    return this.fb.group({
      ingredientName: ['']
    });
  }

  clearIngredients() {
    while (this.ingredients.length !== 0) {
      this.ingredients.removeAt(0);
    }
  }

  get ingredients(): FormArray {
    return this.createDishSuggestionForm.get('ingredients') as FormArray;
  }

  sendSuggestedDish(): void {
    const allIngredients = this.ingredients.value
      .map((ingredient: any) => ingredient.ingredientName)
      .filter((item: string | null) => item !== null)
      .map((item: string) => item.trim());

    const suggestedDish: suggestionData = {
      name: this.createDishSuggestionForm.value.title,
      description: this.createDishSuggestionForm.value.description,
      ingredients: allIngredients,
      image: this.createDishSuggestionForm.get('image')?.value || ''
    };
    this.suggestionService.createSuggestion(suggestedDish).subscribe(
      response => {
        console.log('Suggestion created successful:', response);
        this.feedbackService.displayMessage(response.response);
        this.createDishSuggestionForm.reset();
        this.clearIngredients();
      },
      error => {
        console.error('Suggestion created unsuccessful:', error);
        this.feedbackService.displayMessage(error.error.response);
      }
    );

  }

  onImageChange(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      if (file.type !== 'image/png') {
        event.target.value = '';
        this.createDishSuggestionForm.patchValue({image: ''});
        this.feedbackService.displayMessage("Warnung: Bitte wähle ein PNG als Bild");
        return;
      }
      if (file.size > 10 * 1024 * 1024) {
        event.target.value = '';
        this.createDishSuggestionForm.patchValue({image: ''});
        this.feedbackService.displayMessage("Warnung: Das Bild ist größer als die maximale Größe von 10MB");

      } else {
        const reader = new FileReader();
        reader.onload = () => {
          let base64String = reader.result as string;
          base64String = base64String.replace(/^data:image\/[a-z]+;base64,/, '');
          this.createDishSuggestionForm.patchValue({image: base64String});
        };
        reader.readAsDataURL(file);
      }
    }
  }
}
