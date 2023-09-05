import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ApiService} from "../api.service";
import {AppRoutingModule} from "../app-routing.module";
import {Router} from "@angular/router";
import {CookieService} from "ngx-cookie-service";

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.scss']
})
export class RegistrationComponent implements OnInit {
  registrationForm!: FormGroup;

  ngOnInit(): void {
    this.registrationForm = this.formBuilder.group({
      email: new FormControl('', [
        Validators.required,
      ]),
      username: new FormControl('', [
        Validators.required,
        Validators.minLength(4),
      ]),
      password: new FormControl('', [
        Validators.required,
      ]),
      password_confirm: new FormControl('', [
        Validators.required,
      ]),
    });
  }

  constructor(private formBuilder: FormBuilder,
              private apiService: ApiService,
              private cookieService: CookieService,
              private router: Router) {
  }


  private saveTokenToCookie(token: string): void {
    this.cookieService.set('token', token);
  }


  onSubmit(): void {
    if (this.registrationForm.valid) {
      const formData = this.registrationForm.value;
      this.apiService.register(formData).subscribe(
        (response) => {
          this.apiService.login(formData).subscribe(
            (response) => {
              this.saveTokenToCookie(response.access);
            },
            (error) => {
              console.error('Error: ', error);
            }
          );
          this.router.navigate(['main']);
        },
        (error) => {
          console.log('Error: ', error)
        }
      );
    }
  }
}
