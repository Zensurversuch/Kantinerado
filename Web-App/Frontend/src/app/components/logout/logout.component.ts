import {Component} from '@angular/core';
import {FormsModule} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {AuthService} from "../../service/authentication/auth.service";
import {Router} from "@angular/router";

@Component({
  selector: 'app-logout',
  standalone: true,
  imports: [
    FormsModule,
    HeaderComponent
  ],
  templateUrl: './logout.component.html',
  styleUrl: './logout.component.scss'
})
export class LogoutComponent {
  constructor(private authService: AuthService, private router: Router) {
  }

  logout() {
    this.authService.logout(); // Logout aufrufen
    this.router.navigate(['/login']);
  }
}
