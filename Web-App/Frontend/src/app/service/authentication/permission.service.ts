import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    //Set the permissions for the users here
    'admin': ['createDish', 'hello', 'userOrderSummary'],
    'hungernde': ['hello', 'userOrderSummary'],
    'kantinenmitarbeiter': ['createDish', 'hello', 'userOrderSummary']
  };

  getPermissionsForRole(role: string): string[] {
    return this.permissionsData[role] || [];
  }
}