import {Component} from '@angular/core';
import {MenuComponent} from "../menu/menu.component";
import {NgIf, NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";
import { EventEmitter, Output } from '@angular/core';
import { SettingsComponent } from '../settings/settings.component';




@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss'],
    standalone: true,
  imports: [
    MenuComponent,
    SettingsComponent,
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
  isSettingsOpen: boolean = false;

  @Output() menuOrSettingsToggled: EventEmitter<boolean> = new EventEmitter<boolean>();

  toggleMenu() {
    this.isSettingsOpen = false;
    this.isMenuOpen = !this.isMenuOpen;
    this.menuOrSettingsToggled.emit(this.isMenuOpen);
  }

  toggleSettings() {
    this.isMenuOpen = false;
    this.isSettingsOpen = !this.isSettingsOpen;
    this.menuOrSettingsToggled.emit(this.isSettingsOpen);
  }

  navigateToHome() {
    this.router.navigate(['/']);
  }
}
