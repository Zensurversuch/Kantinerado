import {Routes} from '@angular/router';
import {LoginComponent} from "./components/login/login.component";
import {HelloComponent} from "./components/hello/hello.component";
import {HomeComponent} from "./components/home/home.component";
import {RegisterComponent} from "./components/register/register.component";
import {UserOrderSummaryComponent} from "./components/order_summary/userOrderSummary.component"
import {WorkerOrderSummaryComponent} from "./components/order_summary/workerOrderSummary.component"
import { CreateDishComponent } from './components/dish/createDish.component';
import { AuthGuard } from './guard/auth.guard';
import { RegisterAdminComponent } from './components/register/registerAdmin.component';
import {LogoutComponent} from "./components/logout/logout.component";
import {CreateMealPlanComponent} from "./components/meal_plan/create-meal-plan.component";
import {CreateSuggestionComponent} from "./components/dish_suggestion/createSuggestion.component";
import {ReviewSuggestionComponent} from "./components/dish_suggestion/reviewSuggestion.component";



export const routes: Routes = [
  { path: 'register', component: RegisterComponent},
  { path: 'login', component: LoginComponent},
  { path: 'logout', component: LogoutComponent},
  { path: 'createDish', component: CreateDishComponent, canActivate: [AuthGuard]},
  { path: 'dishSuggestion', component: CreateSuggestionComponent, canActivate: [AuthGuard]},
  { path: 'suggestionReview', component: ReviewSuggestionComponent, canActivate: [AuthGuard] },
  { path: 'createMealPlan', component: CreateMealPlanComponent, canActivate: [AuthGuard]},
  { path: 'hello', component: HelloComponent, canActivate: [AuthGuard]},
  { path: 'userOrderSummary', component: UserOrderSummaryComponent, canActivate: [AuthGuard]},
  { path: 'workerOrderSummary', component: WorkerOrderSummaryComponent, canActivate: [AuthGuard]},
  { path: 'registerAdmin', component: RegisterAdminComponent, canActivate: [AuthGuard]},
  { path: '', component: HomeComponent},

];
