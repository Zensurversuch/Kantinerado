import {Component, HostListener} from '@angular/core';
import {trigger, state, style, animate, transition} from '@angular/animations';
import {MenuComponent} from "../menu/menu.component";


@Component({
    selector: 'app-header',
    templateUrl: './header.component.html',
    styleUrls: ['./header.component.scss'],
    standalone: true,
    imports: [
        MenuComponent
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
export class HeaderComponent {
    username?: string;

    constructor() {
    }

    menuState = 'in';

    toggleMenu() {
        this.menuState = this.menuState === 'out' ? 'in' : 'out';
    }

    @HostListener('document:click', ['$event'])
    clickout(event: any) {
        if (!event.target.closest('.menu')) {
            this.menuState = 'out';
        }
    }
}
