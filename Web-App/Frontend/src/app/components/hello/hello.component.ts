import { Component } from '@angular/core';
import {Router} from "@angular/router";
import {FormsModule} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from '../../authentication/auth.service'
@Component({
  selector: 'app-hello',
  standalone: true,
  imports: [
    FormsModule,
    HeaderComponent
  ],
  templateUrl: './hello.component.html',
  styleUrl: './hello.component.scss'
})
export class HelloComponent {
  helloResponse: string = '';
  constructor(private router: Router, private http: HttpClient, private authService: AuthService) {
  }
  public onSubmit() {
        const headers = new HttpHeaders().set('Authorization', `Bearer ${this.authService.getJwtToken()}`);
        this.http.get('http://185.233.106.149:5000/hello', { headers })
        .subscribe(
          (helloResponse) => {
            console.log('GET request successful', helloResponse);
            this.helloResponse = JSON.stringify(helloResponse);
          },
          (error) => {
            console.error('Error occurred:', error);
            this.helloResponse = JSON.stringify(error);
          }
        );
  }
}
