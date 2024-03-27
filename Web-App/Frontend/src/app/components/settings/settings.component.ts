import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpHeaders } from '@angular/common/http';
import { AllergyService } from '../../service/allergy/allergy.service';
import { AuthService } from '../../service/authentication/auth.service';
import { HeaderComponent } from '../header/header.component';
import { FeedbackService } from '../../service/feedback/feedback.service';

interface Allergy {
  name: string;
  selected: boolean;
}

@Component({
  selector: 'app-settings',
  templateUrl: './settings.component.html',
  styleUrls: ['./settings.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    FormsModule
  ]
})
export class SettingsComponent implements OnInit {
  allergies: Allergy[] = [];
  darkMode: boolean = false;
  headers: HttpHeaders;

  constructor(private allergyService: AllergyService, private authService: AuthService, private header: HeaderComponent, private feedbackService: FeedbackService) {
    this.headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
  }

  ngOnInit(): void {
  const storedDarkMode = localStorage.getItem('darkMode');
    if (storedDarkMode !== null) {
      this.darkMode = JSON.parse(storedDarkMode);
    }

    this.allergyService.getAllergies().subscribe(
      (response: any[]) => {
        this.allergies = response.map((allergy: any) => ({ name: allergy.name, selected: false}));
        console.log(this.allergies)
        this.setUsersAllergies();
      },
      error => {
        console.error('Error fetching allergies:', error);
        this.allergies = [{ name: "Error Loading Allergies", selected: true }];
      }
    );
  }

  closeSettings() {
    this.header.toggleSettings();
  }


  toggleDarkMode() {
    // Hier Logik für Dark mode einfügen
    this.darkMode = !this.darkMode;
    localStorage.setItem('darkMode', JSON.stringify(this.darkMode));
    console.log('Dark Mode wurde umgeschaltet!');
  }

  toggleAllergy(allergy: Allergy) {
    allergy.selected = !allergy.selected;
  }


  setUsersAllergies(): void {
    const userID = this.authService.getUserID();
    // Fetch user's allergies
    this.allergyService.getAllergiesByUser(userID, this.headers).subscribe(
      (userAllergies: string[]) => {
        // Set user's allergies to true
        userAllergies.forEach((userAllergy: string) => {
          const index = this.allergies.findIndex(allergy => allergy.name === userAllergy);
          if (index !== -1) {
            this.allergies[index].selected = true;
          }
        });
      },
      error => {
        console.error('Error fetching user allergies:', error);
        this.feedbackService.displayMessage(error.error.response);
      }
    );
  }



  submitAllergies() {
    const selectedAllergies: Allergy[] = this.allergies.filter(allergy => allergy.selected);
    const selectedAllergiesNames: string[] = selectedAllergies.map(allergy => allergy.name);
    const chosen_allergies = { allergies: selectedAllergiesNames };
    console.log('Ausgewählte Allergien:', chosen_allergies);
  
    this.allergyService.setAllergies(chosen_allergies, this.headers).subscribe(
      response => {
        this.feedbackService.displayMessage(response.response);
      },
      error => {
        this.feedbackService.displayMessage(error.error.response);
      }
    );
  }

}