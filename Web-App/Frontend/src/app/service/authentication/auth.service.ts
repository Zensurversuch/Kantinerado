import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private jwtToken: string | null = null;
  private userRole: string | null = null;

  constructor() { }

  setJwtToken(token: string) {
    this.jwtToken = token;
  }

  getJwtToken(): string | null {
    return this.jwtToken;
  }

  setUserRole(role: string) {
    this.userRole = role;
  }

  getUserRole(): string | null {
    return this.userRole;
  }

  isLoggedIn(): boolean {
    return !!this.jwtToken;
  }

  logout() {
    this.jwtToken = null;
    this.userRole = null;
  }
}