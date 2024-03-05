import { Routes } from '@angular/router';
import {LoginComponent} from "./components/login/login.component";
import {HelloComponent} from "./components/hello/hello.component";
import {HomeComponent} from "./components/home/home.component";
import {RegisterComponent} from "./components/register/register.component";
import { CreateDishComponent } from './components/dish/createDish.component';


export const routes: Routes = [
  {path: 'register', component: RegisterComponent},
  { path: 'login', component: LoginComponent},
  { path: 'createDish', component: CreateDishComponent},
  { path: 'hello', component: HelloComponent},
  { path: '', component: HomeComponent}
];
