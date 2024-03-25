import {Component} from '@angular/core';
import {FormControl, FormGroup, FormsModule, isFormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {NgIf} from "@angular/common";
import {UserData} from '../../interface/user-data';
import {UserService} from '../../service/user/user.service';
import {HttpClientModule} from "@angular/common/http";
import {PasswordValidator} from "./password-validator";
import {Role} from "../../interface/role";
import { FeedbackService } from '../../service/feedback/feedback.service';


@Component({
  selector: 'app-register',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    FormsModule,
    HeaderComponent,
    NgIf,
    HttpClientModule
  ],
  templateUrl: './register.component.html',
  styleUrl: './register.component.scss'
})
export class RegisterComponent {
  REGEX_PASSWORD: RegExp = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!^_%*#?&])[A-Za-z\d@$!_%*#?&]{8,}$/;
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
        Validators.pattern(this.REGEX_PASSWORD),
      ],
      [])
  },{ validators: PasswordValidator } );

  constructor(private userService: UserService, private feedbackService: FeedbackService) {
    this.registerForm.valueChanges.subscribe(console.log)

  }

  registerUser() {
    if (this.registerForm.valid) {
      const userData: UserData = {
        firstName: this.registerForm.value.firstname,
        lastName: this.registerForm.value.lastname,
        email: this.registerForm.value.email,
        password: this.registerForm.value.password,
        role: Role.hungernde
      };

      this.userService.createUser(userData).subscribe(
        response => {
          this.feedbackService.displayMessage(response.response);
          console.log('Benutzer wurde erfolgreich erstellt:', response);
        },
        error => {
          console.error('Fehler beim Erstellen des Benutzers:', error);
          this.feedbackService.displayMessage(error.error.response);
        }
      );
    } else {

    }
  }

  protected readonly isFormControl = isFormControl;
  protected readonly parent = parent;
}
