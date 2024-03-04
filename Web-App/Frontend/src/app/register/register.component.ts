import {Component} from '@angular/core';
import {FormControl, FormGroup, FormsModule, isFormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    FormsModule,
    HeaderComponent,
    NgIf
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  REGEX_PASSWORD: RegExp = /^(?=[^A-Z]*[A-Z])(?=[^a-z]*[a-z])(?=\D*\d).{8,}$/;
  public registerForm: FormGroup = new FormGroup({
    lastname: new FormControl('',
      [
        Validators.required
      ],
      []),
    firstname: new FormControl('',
      [
        Validators.required
      ],
      []),
    email: new FormControl('',
      [
        Validators.required,
        Validators.email
      ],
      []),
    password: new FormControl('',
      [
        Validators.required,
        Validators.minLength(8),
        Validators.maxLength(50),
        Validators.pattern(this.REGEX_PASSWORD)
      ],
      []),
    confirmpassword: new FormControl('',
      [
        Validators.required,
        Validators.minLength(8),
        Validators.maxLength(50),
        Validators.pattern(this.REGEX_PASSWORD)
      ],
      [])
  })

  constructor() {
    this.registerForm.valueChanges.subscribe(console.log)

  }

  register() {
  }

  protected readonly isFormControl = isFormControl;
  protected readonly parent = parent;
}
