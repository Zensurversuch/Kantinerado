import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {FormsModule} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../authentication/auth.service'
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
  public onSubmit() {
    const userData = {
      email: this.username,
      password: this.password
    };

    this.http.post('http://localhost:5000/login', userData)
    .subscribe(
      (response: any) => {
        console.log('POST request successful', response);
        this.authService.setJwtToken(response.access_token);
        console.log('POST request successful', this.authService.getJwtToken());
        this.router.navigate(['/hello']);
      },
      (error) => {
        console.error('Error occurred:', error);
        // Handle error as needed
      }
    );
  }
}
