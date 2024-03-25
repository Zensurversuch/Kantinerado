import {Component, OnInit} from '@angular/core';

import {RouterLink} from "@angular/router";
import {AuthService} from "../../service/authentication/auth.service";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  standalone: true,
  imports: [
    RouterLink,
    NgIf
  ],

})
export class MenuComponent implements OnInit{
  userRole: string | null;
  isLoggedIn: boolean;

  constructor(private authService: AuthService) {
    this.isLoggedIn=false;
    this.userRole=null;
  }
  ngOnInit(): void {
    this.userRole = this.authService.getUserRole();
    this.isLoggedIn = this.authService.isLoggedIn();
  }
}
