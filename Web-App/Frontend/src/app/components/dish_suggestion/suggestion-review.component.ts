import {Component, OnInit} from '@angular/core';
import {Suggestion} from "../../interface/suggestion";
import {SuggestionService} from "../../service/suggestion/suggestion.service";
import {ReactiveFormsModule} from "@angular/forms";
import {SuggestionCard} from "./suggestion-card.component";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-suggestion-review',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    SuggestionCard,
    NgForOf
  ],
  templateUrl: './suggestion-review.component.html',
  styleUrl: './suggestion.component.scss'
})
export class SuggestionReviewComponent implements OnInit{
  suggestions: Suggestion[] = [];

  constructor(private suggestionService: SuggestionService){}

  ngOnInit(): void {
    this.loadSuggestions();
  }

  loadSuggestions(): void {
    this.suggestionService.getAllSuggestions().subscribe(
      data => this.suggestions = data,
      error => console.error('Fehler beim Laden der Gerichtsvorschläge', error)
    );
  }
}
