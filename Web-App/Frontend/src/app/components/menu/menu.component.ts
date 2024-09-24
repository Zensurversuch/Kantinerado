import {Component, OnInit} from '@angular/core';

import {RouterLink} from "@angular/router";
import {AuthService} from "../../service/authentication/auth.service";
import {NgIf, NgOptimizedImage} from "@angular/common";
import { Role } from '../../interface/role';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  standalone: true,
  imports: [
    RouterLink,
    NgIf,
    NgOptimizedImage
  ],

})
export class MenuComponent implements OnInit{
  userRole: string | null;
  isLoggedIn: boolean;
  admin: string;
  hungernde: string;
  kantinenmitarbeiter: string;


  constructor(private authService: AuthService) {
    this.isLoggedIn=false;
    this.userRole=null;
    this.admin=Role.admin;
    this.hungernde=Role.hungernde;
    this.kantinenmitarbeiter=Role.kantinenmitarbeiter;
  }
  ngOnInit(): void {
    this.userRole = this.authService.getUserRole();
    this.isLoggedIn = this.authService.isLoggedIn();
  }
}
