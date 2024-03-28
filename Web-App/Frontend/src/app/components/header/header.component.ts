import {Component} from '@angular/core';
import {MenuComponent} from "../menu/menu.component";
import {NgIf, NgOptimizedImage} from "@angular/common";
import {Router} from "@angular/router";
import { EventEmitter, Output } from '@angular/core';
import { SettingsComponent } from '../settings/settings.component';
import { AuthService } from '../../service/authentication/auth.service';




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

  constructor(private router:Router, private authService: AuthService) {
    this.isLoggedIn=false;
  }

  menuState = 'in';
  isLoggedIn: boolean;
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

  ngOnInit(): void {
    this.isLoggedIn = this.authService.isLoggedIn();
  }
}
