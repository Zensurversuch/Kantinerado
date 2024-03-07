import { Injectable } from '@angular/core';
import { Role } from '../../interface/role';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    [Role.admin]: ['createDish', 'hello', 'registerAdmin', 'userOrderSummary'],
    [Role.hungernde]: ['hello', 'userOrderSummary'],
    [Role.kantinenmitarbeiter]: ['createDish', 'hello']
  };

  getPermissionsForRole(role: string): string[] {
    return this.permissionsData[role] || [];
  }

  public getRoles(): string[] {
    return Object.keys(this.permissionsData);
  }
}