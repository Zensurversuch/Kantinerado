import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    'admin': ['hello', 'createDish'],
    'hungernde': ['hello'],
    'kantinenmitarbeiter': ['hello', 'createDish']
  };

  getPermissionsForRole(role: string): string[] {
    return this.permissionsData[role] || [];
  }
}