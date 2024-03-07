import { Injectable } from '@angular/core';
import { Role } from '../../interface/role';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    [Role.admin]: ['createDish', 'hello', 'registerAdmin', 'userOrderSummary', 'workerOrderSummary'],
    [Role.hungernde]: ['hello', 'userOrderSummary'],
    [Role.kantinenmitarbeiter]: ['createDish', 'hello', 'workerOrderSummary']
  };

  getPermissionsForRole(role: string): string[] {
    console.log(this.permissionsData[role] );
    console.log(this.permissionsData);
    return this.permissionsData[role] || [];
  }

  public getRoles(): string[] {
    return Object.keys(this.permissionsData);
  }
}