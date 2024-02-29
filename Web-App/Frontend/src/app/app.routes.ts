import { Routes } from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {HomeComponent} from "./home/home.component";
import {RegisterComponent} from "./register/register.component";

export const routes: Routes = [
  {path: 'registration', component: RegisterComponent},
  { path: 'login', component: LoginComponent},
  { path: '', component: HomeComponent}
];
