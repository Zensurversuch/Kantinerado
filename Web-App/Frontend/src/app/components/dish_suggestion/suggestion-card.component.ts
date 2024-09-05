import { Component } from '@angular/core';
import {CommonModule} from "@angular/common";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {Input } from '@angular/core';
import {Suggestion} from '../../interface/suggestion';
@Component({
  selector: 'app-suggestion-card',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './suggestion-card.component.html',
  styleUrl: './suggestion.component.scss'
})
export class SuggestionCard {


  @Input() suggestion: Suggestion | undefined;

  isOpen = false;

  onSubmit() {
    // Logik zum Speichern des Gerichts
  }

  onReject() {
    // Logik zum Ablehnen des Vorschlags
  }
}

