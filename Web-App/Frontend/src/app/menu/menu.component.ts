import { Component } from '@angular/core';
import { trigger, state, style, animate, transition } from '@angular/animations';
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  standalone: true,
  imports: [
    RouterLink
  ],
  animations: [
    trigger('slideMenu', [
      state('in', style({transform: 'translateX(0)'})),
      state('out', style({transform: 'translateX(-100%)'})),
      transition('in => out', animate('300ms ease-in')),
      transition('out => in', animate('300ms ease-out'))
    ])
  ]
})
export class MenuComponent {
  menuState = 'in';
  menuClick(event: MouseEvent) {
    event.stopPropagation();
  }
}
