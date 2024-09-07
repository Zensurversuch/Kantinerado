import {Component, OnInit} from '@angular/core';
import {Suggestion} from "../../interface/suggestion";
import {SuggestionService} from "../../service/suggestion/suggestion.service";
import {ReactiveFormsModule} from "@angular/forms";
import {SuggestionCard} from "./suggestion-card.component";
import {NgForOf, NgIf} from "@angular/common";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-suggestion-review',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    SuggestionCard,
    NgForOf,
    HeaderComponent,
    SuggestionCard,
    NgIf
  ],
  templateUrl: './suggestion-review.component.html',
  styleUrl: './suggestion-card.scss'
})
export class SuggestionReviewComponent implements OnInit{
  blurred: boolean = false;
  suggestions: Suggestion[] = [];
  loading: boolean = true;

  constructor(private suggestionService: SuggestionService){}

  ngOnInit(): void {
    this.loadSuggestions();
  }

  loadSuggestions(): void {
    this.suggestionService.getAllSuggestions().subscribe(
      data => {
        this.suggestions = data;
        this.loading = false;
        console.log(this.suggestions);
      },
      error => {
        console.error('Fehler beim Laden der Gerichtsvorschläge', error);
        this.loading = false;
      }
    );
  }
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
  }
}
