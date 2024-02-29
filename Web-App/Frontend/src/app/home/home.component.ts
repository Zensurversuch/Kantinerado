import { Component } from '@angular/core';
import {HeaderComponent} from "../header/header.component";
import {MenuComponent} from "../menu/menu.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    HeaderComponent,
    MenuComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.scss'
})
export class HomeComponent {

}
