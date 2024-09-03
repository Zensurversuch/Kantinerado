import {Component, OnInit} from '@angular/core';
import {Suggestion} from "../../interface/suggestion";
import {SuggestionService} from "../../service/suggestion/suggestion.service";
import {FormBuilder, FormGroup, ReactiveFormsModule, Validators} from "@angular/forms";

@Component({
  selector: 'app-suggestion-review',
  standalone: true,
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './suggestion-review.component.html',
  styleUrl: './suggestion.component.scss'
})
export class SuggestionReviewComponent implements OnInit{
  suggestions: Suggestion[] = [];
  selectedSuggestion?: Suggestion;
  dishForm: FormGroup;

  constructor(
    private suggestionService: SuggestionService,
    private fb: FormBuilder
  ) {
    this.dishForm = this.fb.group({
      price: ['', Validators.required],
      dietaryCategory: ['', Validators.required],
      mealType: ['', Validators.required],
      allergies: this.fb.array([])  // Hier können wir eine Liste der Allergien erfassen
    });
  }

  ngOnInit(): void {
    this.loadSuggestions();
  }

  loadSuggestions(): void {
    this.suggestionService.getAllSuggestions().subscribe(
      data => this.suggestions = data,
      error => console.error('Fehler beim Laden der Gerichtsvorschläge', error)
    );
  }

  onSelectSuggestion(suggestion: Suggestion): void {
    this.selectedSuggestion = suggestion;
    // Felder im Formular vorbefüllen, falls nötig
    this.dishForm.patchValue({
      // Vorbefüllen mit Daten, falls verfügbar
    });
  }

  onSubmit(): void {
    if (this.dishForm.valid && this.selectedSuggestion) {
      const suggestionData = {
        //dishSuggestionID: this.selectedSuggestion.id,
        ...this.dishForm.value,
        name: this.selectedSuggestion.name,
        ingredients: this.selectedSuggestion.ingredients,
        image: this.selectedSuggestion.image
      };

      this.suggestionService.acceptSuggestion(suggestionData).subscribe(
        response => {
          console.log('Gericht erfolgreich erstellt', response);
          this.loadSuggestions(); // Aktualisieren der Liste nach dem Akzeptieren
        },
        error => console.error('Fehler beim Erstellen des Gerichts', error)
      );
    }
  }


  toggleDetails() {

  }

  onReject() {

  }
}
