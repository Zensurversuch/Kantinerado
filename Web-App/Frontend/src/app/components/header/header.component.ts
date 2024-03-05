import {Component} from '@angular/core';
import {MenuComponent} from "../menu/menu.component";
import {NgIf, NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";



@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss'],
    standalone: true,
  imports: [
    MenuComponent,
    NgOptimizedImage,
    NgIf
  ],
})
export class HeaderComponent {
    username?: string;

    constructor(private router:Router) {
    }

    menuState = 'in';

  isMenuOpen: boolean = false;

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

  navigateToHome() {
    this.router.navigate(['/']);
  }
}
