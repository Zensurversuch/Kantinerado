import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; 
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AllergyService } from '../../service/allergy/allergy.service';
import { AuthService } from '../../service/authentication/auth.service';
import { environment } from '../../../environments/environment';

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

  constructor(private allergyService: AllergyService, private http: HttpClient, private authService: AuthService) {
    this.allergyService.getAllergies().subscribe(
      (response: any[]) => {
        this.allergies = response.map((allergy: any) => ({ name: allergy.name, selected: false}));
        console.log(this.allergies)
      },
      error => {
        console.error('Error fetching allergies:', error);
        this.allergies = [{ name: "Error Loading Allergies", selected: true }];
      }
    );
  }

  ngOnInit(): void {
    // Lade den Darkmode-Wert aus dem localStorage, wenn vorhanden
    const storedDarkMode = localStorage.getItem('darkMode');
    if (storedDarkMode !== null) {
      this.darkMode = JSON.parse(storedDarkMode);
    }
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

  submitAllergies() {
    const selectedAllergies: Allergy[] = this.allergies.filter(allergy => allergy.selected);
    const selectedAllergiesNames: string[] = selectedAllergies.map(allergy => allergy.name);
    const chosen_allergies = { allergies: selectedAllergiesNames };
    console.log('Ausgewählte Allergien:', chosen_allergies);
  
    const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
    this.http.post<any>(environment.apiUrl + '/create_allergies', chosen_allergies, { headers })
      .subscribe(
        response => {
          // Handle response if needed
          console.log('Response from server:', response);
        },
        error => {
          // Handle error if needed
          console.error('Error while submitting allergies:', error);
        }
      );
  }
  
}