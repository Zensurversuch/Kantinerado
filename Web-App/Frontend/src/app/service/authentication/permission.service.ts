import { Injectable } from '@angular/core';
import { Role } from '../../interface/role';

@Injectable({
  providedIn: 'root'
})

export class PermissionService {
  private permissionsData: { [key: string]: string[] } = {
    [Role.admin]: ['createDish', 'hello', 'registerAdmin', 'userOrderSummary', 'workerOrderSummary', 'createMealPlan', 'dishSuggestion', 'suggestionReview'],
    [Role.hungernde]: ['hello', 'userOrderSummary', 'dishSuggestion'],
    [Role.kantinenmitarbeiter]: ['createDish', 'hello', 'workerOrderSummary', 'createMealPlan', 'suggestionReview']
  };

  getPermissionsForRole(role: string): string[] {
    return this.permissionsData[role] || [];
  }

  public getRoles(): string[] {
    return Object.keys(this.permissionsData);
  }
}
