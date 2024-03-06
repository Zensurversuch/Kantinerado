import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {FormsModule} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import { HttpClient } from '@angular/common/http';
import {environment} from "../../../environments/environment";
import { AuthService } from '../../service/authentication/auth.service';
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    FormsModule,
    HeaderComponent
  ],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss'
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  constructor(private router: Router, private http: HttpClient, private authService: AuthService) {
  }
  public submit_login() {
    const userData = {
      email: this.username,
      password: this.password
    };

    this.http.post(environment.apiUrl+'/login', userData)
    .subscribe(
      (response: any) => {
        console.log('POST request successful', response);
        this.authService.setJwtToken(response.access_token);
        console.log('POST request successful', this.authService.getJwtToken());
        this.router.navigate(['/hello']);
        this.authService.setUserRole("hungernde"); // Setzen der Rolle des Benutzers muss noch implementiert werden
      },
      (error) => {
        console.error('Error occurred:', error);
        // Handle error as needed
      }
    );
  }

  navigateToRegister() {
    this.router.navigate(['/register']); // Navigieren zur Registrierungsseite
  }
}
