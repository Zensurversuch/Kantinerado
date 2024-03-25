import {Component, OnInit} from '@angular/core';

import {RouterLink} from "@angular/router";
import {AuthService} from "../../service/authentication/auth.service";
import {NgIf} from "@angular/common";
import { Role } from '../../interface/role';
import { PermissionService } from '../../service/authentication/permission.service';

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
  admin: string;
  hungernde: string;
  kantinenmitarbeiter: string;


  constructor(private authService: AuthService, private permissionService: PermissionService) {
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
