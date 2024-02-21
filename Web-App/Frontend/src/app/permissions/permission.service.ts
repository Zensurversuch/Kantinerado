import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    'admin': ['money', 'users', 'products'],
    'hungernder': ['products'],
    'kantinenmitarbeiter': ['food', 'orders']
  };

  constructor() { }

  getPermissionsForRole(role: string): string[] {
    return this.permissionsData[role] || [];
  }
}