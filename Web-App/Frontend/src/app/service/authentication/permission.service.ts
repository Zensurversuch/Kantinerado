import { Injectable } from '@angular/core';
import { Role } from '../../interface/role';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    [Role.admin]: ['createDish', 'hello', 'registerAdmin'],
    [Role.hungernde]: ['hello'],
    [Role.kantinenmitarbeiter]: ['createDish', 'hello']
  };

  getPermissionsForRole(role: string): string[] {
    return this.permissionsData[role] || [];
  }

  public getRoles(): string[] {
    return Object.keys(this.permissionsData);
  }
}