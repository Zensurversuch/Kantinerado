import {Component, OnInit} from '@angular/core';
import {FormControl, FormGroup, FormsModule, isFormControl, ReactiveFormsModule, Validators} from "@angular/forms";
import {HeaderComponent} from "../header/header.component";
import {CommonModule, NgIf} from "@angular/common";
import {UserData} from '../../interface/user-data';
import {UserService} from '../../service/user/user.service';
import {HttpClientModule} from "@angular/common/http";
import {PasswordValidator} from "./password-validator";
import { PermissionService } from '../../service/authentication/permission.service';


@Component({
  selector: 'app-registerAdmin',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    FormsModule,
    HeaderComponent,
    NgIf,
    HttpClientModule,
    CommonModule
  ],
  templateUrl: './registerAdmin.component.html',
  styleUrl: './registerAdmin.component.scss'
})
export class RegisterAdminComponent  {
  roles = this.permissionService.getRoles();
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
    role: new FormControl('',
      [
        Validators.required,
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

  constructor(private userService: UserService, private permissionService: PermissionService) {
    this.registerForm.valueChanges.subscribe(console.log)
  }

  blurred: boolean = false;
  ToggleBlurred(isOpened: boolean) {
    this.blurred = isOpened;
  }

  registerAdmin() {
    if (this.registerForm.valid) {
      const userData: UserData = {
        firstName: this.registerForm.value.firstname,
        lastName: this.registerForm.value.lastname,
        email: this.registerForm.value.email,
        password: this.registerForm.value.password,
        role: this.registerForm.value.role,
      };

      this.userService.createAdmin(userData).subscribe(
        response => {
          console.log('Benutzer wurde erfolgreich erstellt:', response);
        },
        error => {
          console.error('Fehler beim Erstellen des Benutzers:', error);

        }
      );
    } else {

    }
  }

  protected readonly isFormControl = isFormControl;
  protected readonly parent = parent;
}
