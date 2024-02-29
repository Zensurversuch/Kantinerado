import {Component} from '@angular/core';
import {MenuComponent} from "../menu/menu.component";
import {NgIf, NgOptimizedImage} from "@angular/common";


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

    constructor() {
    }

    menuState = 'in';

  isMenuOpen: boolean = false;

  toggleMenu() {
    this.isMenuOpen = !this.isMenuOpen;
  }

}
