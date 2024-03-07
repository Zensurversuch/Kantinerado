import { Routes } from '@angular/router';
import {LoginComponent} from "./components/login/login.component";
import {HelloComponent} from "./components/hello/hello.component";
import {HomeComponent} from "./components/home/home.component";
import {RegisterComponent} from "./components/register/register.component";
import {UserOrderSummaryComponent} from "./components/order_summary/userOrderSummary.component"
import { CreateDishComponent } from './components/dish/createDish.component';
import { AuthGuard } from './guard/auth.guard';
import { RegisterAdminComponent } from './components/register/registerAdmin.component';


export const routes: Routes = [
  {path: 'register', component: RegisterComponent},
  { path: 'login', component: LoginComponent},
  { path: 'createDish', component: CreateDishComponent, canActivate: [AuthGuard]},
  { path: 'hello', component: HelloComponent, canActivate: [AuthGuard]},
  { path: 'userOrderSummary', component: UserOrderSummaryComponent, canActivate: [AuthGuard]},
  { path: 'registerAdmin', component: RegisterAdminComponent, canActivate: [AuthGuard]},
  { path: '', component: HomeComponent}
];
