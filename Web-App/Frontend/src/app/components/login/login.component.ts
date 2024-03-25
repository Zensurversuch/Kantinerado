import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { HeaderComponent } from '../header/header.component';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environment';
import { AuthService } from '../../service/authentication/auth.service';
import { FeedbackService } from '../../service/feedback/feedback.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule, HeaderComponent],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']

})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(
    private router: Router,
    private http: HttpClient,
    private authService: AuthService,
    private feedbackService: FeedbackService
  ) {}

  public submit_login() {
    const userData = {
      email: this.username,
      password: this.password
    };

    this.http.post(environment.apiUrl + '/login', userData).subscribe(
      (response: any) => {
        this.feedbackService.displayMessage(response.response);
        console.log('POST request successful', response);
        this.authService.setJwtToken(response.access_token);
        this.router.navigate(['/']);
        this.authService.setUserRole(response.role);
        this.authService.setUserID(response.userID);
      },
      (error) => {
        console.error(error.error.response);
        this.feedbackService.displayMessage(error.error.response);
      }
    );
  }

  navigateToRegister() {
    this.router.navigate(['/register']);
  }
}
