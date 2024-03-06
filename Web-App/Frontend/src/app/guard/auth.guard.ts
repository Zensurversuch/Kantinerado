import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, CanActivate, Router, UrlSegment } from '@angular/router';
import { AuthService } from '../service/authentication/auth.service';
import { PermissionService } from '../service/authentication/permission.service';


@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(
    private authService: AuthService,
    private permissionService: PermissionService,
    private router: Router
  ) { }

  canActivate(route: ActivatedRouteSnapshot): boolean {
    const token = this.authService.getJwtToken();
    if (!token || this.authService.isTokenExpired()) {
        this.authService.logout();
        return false;
    }

    const userRole = this.authService.getUserRole();
    if (!userRole) {
        return false;
    }
    
    const rolePermissions = this.permissionService.getPermissionsForRole(userRole);
    const routePermission = this.getRoutePermission(route);
    if (!rolePermissions.includes(routePermission)) {
        this.router.navigate(['/login']);
        return false;
    }

    return true;
  }

  private getRoutePermission(route: ActivatedRouteSnapshot): string {
    const urlSegments: UrlSegment[] = route.url;
    const mainRoute = urlSegments.length > 0 ? urlSegments[0].path : '';
    return mainRoute;
  }
}