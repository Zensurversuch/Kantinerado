import { Injectable } from '@angular/core';
import { jwtDecode } from 'jwt-decode';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly TOKEN_KEY = 'jwtToken';
  private readonly USER_ROLE_KEY = 'userRole';
  private readonly USER_ID_KEY = 'userID';
  private jwtToken: string | null = null;
  private userRole: string | null = null;
  private userID: string | null = null;


  constructor() {
    this.jwtToken = sessionStorage.getItem(this.TOKEN_KEY); 
    this.userRole = sessionStorage.getItem(this.USER_ROLE_KEY);
    this.userID = sessionStorage.getItem(this.USER_ID_KEY);
  }

  setJwtToken(token: string) {
    this.jwtToken = token;
    sessionStorage.setItem(this.TOKEN_KEY, token); 
  }

  getJwtToken(): string | null {
    if (!this.jwtToken) {
      this.jwtToken = sessionStorage.getItem(this.TOKEN_KEY); 
    }
    return this.jwtToken;
  }

  isTokenExpired(): boolean {
    const token = this.getJwtToken();
    if (token) {
      const tokenPayload = jwtDecode(token); 
      const expiryTime = (tokenPayload.exp as number) * 1000; 
      return Date.now() >= expiryTime;
    }
    return true;
  }

  setUserRole(role: string) {
    this.userRole = role;
    sessionStorage.setItem(this.USER_ROLE_KEY, role);
  }

  getUserRole(): string | null {
    if (!this.userRole) {
      this.userRole = sessionStorage.getItem(this.USER_ROLE_KEY);
    }
    return this.userRole;
  }

  setUserID(userID: string) {
    this.userID = userID;
    sessionStorage.setItem(this.USER_ID_KEY, userID);
  }

  getUserID(): string | null {
    if (!this.userID) {
      this.userID = sessionStorage.getItem(this.USER_ID_KEY);
    }
    return this.userID;
  }

  isLoggedIn(): boolean {
    return !!this.jwtToken;
  }

  logout() {
    this.jwtToken = null;
    this.userRole = null;
    this.userID = null;
    sessionStorage.removeItem(this.TOKEN_KEY);
    sessionStorage.removeItem(this.USER_ID_KEY);
    sessionStorage.removeItem(this.USER_ROLE_KEY);
  }
}