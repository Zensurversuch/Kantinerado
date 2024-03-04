import { Routes } from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {HelloComponent} from "./hello/hello.component";
import {HomeComponent} from "./home/home.component";
import {RegisterComponent} from "./register/register.component";


export const routes: Routes = [
  {path: 'register', component: RegisterComponent},
  { path: 'login', component: LoginComponent},
  { path: 'hello', component: HelloComponent},
  { path: '', component: HomeComponent}
];
